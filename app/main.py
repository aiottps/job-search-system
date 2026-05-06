import argparse
import sys
import os
import asyncio
from app.utils.encoding import setup_encoding
from app.config import config
from app.schemas.job import JobItem, InterviewGuide
from app.normalizers.salary import parse_salary
from app.normalizers.location import normalize_location
from app.normalizers.work_mode import normalize_work_mode
from app.normalizers.dedupe import calculate_content_hash
from app.db.connection import db_session
from app.db.repository import JobRepository
from app.analyzers.gemini_client import GeminiClient, get_default_analysis
from app.email.sender import EmailSender
from app.collectors.collector_104 import Collector104
from app.collectors.collector_1111 import Collector1111
from app.utils.logger import logger

def get_collectors():
    """Returns a list of active collectors."""
    return [Collector104(), Collector1111()]

async def collect_jobs(mode: str):
    """Collects jobs from mock or real sources based on mode and config."""
    collectors = get_collectors()
    raw_jobs = []
    
    use_real = (mode == "daily" and config.USE_REAL_COLLECTORS)
    
    for collector in collectors:
        try:
            if use_real:
                logger.info(f"Using REAL collector for {collector.__class__.__name__}")
                results = await collector.search_real(
                    config.JOB_KEYWORDS, 
                    config.JOB_LOCATIONS, 
                    max_results=config.MAX_JOBS_PER_SOURCE
                )
            else:
                logger.info(f"Using MOCK collector for {collector.__class__.__name__}")
                results = collector.search(config.JOB_KEYWORDS, config.JOB_LOCATIONS)
            
            raw_jobs.extend(results)
        except Exception as e:
            logger.exception(f"Collector {collector.__class__.__name__} failed: {e}")
            
    return raw_jobs

async def daily_job_search_async(mode="daily"):
    logger.info(f"Starting job search (Mode: {mode})")
    logger.info(f"Flags: USE_DB={config.USE_DB}, USE_GEMINI={config.USE_GEMINI}, SEND_EMAIL={config.SEND_EMAIL}, USE_REAL={config.USE_REAL_COLLECTORS}")
    
    user_prefs = config.user_prefs_text
    
    # 2. Collect jobs
    raw_jobs = await collect_jobs(mode)
    
    processed_jobs = []
    gemini = GeminiClient() if config.USE_GEMINI else None

    def process_job(raw, repo=None):
        try:
            # 3. Create JobItem & Normalize
            job = JobItem(**raw)
            
            salary_res = parse_salary(job.salary_text)
            job.annual_salary_min = salary_res.annual_min
            job.annual_salary_max = salary_res.annual_max
            job.salary_is_estimated = salary_res.is_estimated
            job.salary_note = salary_res.note
            
            job.std_location = normalize_location(job.location)
            job.std_work_mode = normalize_work_mode(job.jd_text, job.location)
            job.content_hash = calculate_content_hash(job)
            
            logger.info(f"Processing: {job.title} @ {job.company_name}")

            # 4. Dedupe & DB Save
            job_id = None
            if repo and config.USE_DB:
                existing_id = repo.find_existing_job(job.source, job.source_job_id, job.content_hash)
                if existing_id:
                    logger.info(f"  [Skip] Duplicate found (ID: {existing_id})")
                    return None
                job_id = repo.save_job(job)
                logger.info(f"  [Save] Job saved to DB (ID: {job_id})")
            else:
                logger.info(f"  [Log] Skipping DB save")

            # 5. AI Analysis
            analysis = None
            if config.USE_GEMINI and gemini:
                logger.info(f"  [AI] Analyzing with Gemini...")
                analysis = gemini.analyze_jd(job.jd_text, user_prefs)
            else:
                logger.info(f"  [AI] Using default analysis")
                analysis = get_default_analysis()

            job_dict = job.model_dump()
            job_dict['analysis'] = analysis
            
            # 6. Save Interview Guide (if DB enabled)
            if repo and config.USE_DB and job_id:
                try:
                    guide = InterviewGuide(
                        job_id=job_id,
                        jd_summary=analysis.get('jd_summary', ''),
                        resume_focus=analysis.get('resume_focus', []),
                        required_skills=analysis.get('required_skills', []),
                        bonus_skills=analysis.get('bonus_skills', []),
                        company_market_analysis=analysis.get('company_market_analysis', ''),
                        mock_questions=analysis.get('mock_questions', []),
                        portfolio_suggestions=analysis.get('portfolio_suggestions', []),
                        risk_warnings=analysis.get('risk_warnings', [])
                    )
                    repo.save_interview_guide(guide)
                except Exception as guide_err:
                    logger.error(f"  [Error] Failed to save interview guide: {guide_err}")

            return job_dict

        except Exception as e:
            logger.error(f"  [Error] Failed to process job: {e}")
            return None

    # Execution Loop
    if config.USE_DB:
        with db_session() as db:
            repo = JobRepository(db)
            for raw in raw_jobs:
                res = process_job(raw, repo)
                if res: processed_jobs.append(res)
    else:
        for raw in raw_jobs:
            res = process_job(raw)
            if res: processed_jobs.append(res)

    # 7. Email Summary
    if processed_jobs:
        if config.SEND_EMAIL:
            logger.info(f"Sending email for {len(processed_jobs)} jobs...")
            sender = EmailSender()
            sender.send_daily_jobs(processed_jobs)
        else:
            logger.info(f"  [Preview] Generating output/email_preview.html")
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            sender = EmailSender()
            template = sender.jinja_env.get_template('daily_jobs_zh_tw.html')
            content = template.render(jobs=processed_jobs)
            preview_path = os.path.join(output_dir, "email_preview.html")
            with open(preview_path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"  [Preview] Preview saved to {preview_path}")
    else:
        logger.info("No new jobs to notify.")
    
    logger.info(f"Job search {mode} completed.")

def main():
    setup_encoding()
    parser = argparse.ArgumentParser(description="Personal Job Search Assistant")
    parser.add_argument("--mode", choices=["daily", "search", "analyze", "mock"], default="daily")
    args = parser.parse_args()

    mode = args.mode
    if mode in ["daily", "mock"]:
        asyncio.run(daily_job_search_async(mode))
    else:
        logger.warning(f"Mode {mode} not implemented yet.")

if __name__ == "__main__":
    main()
