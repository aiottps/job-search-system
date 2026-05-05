from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas.job import JobItem, InterviewGuide
import json

class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_existing_job(self, source: str, source_job_id: str = None, content_hash: str = None):
        if source_job_id:
            query = text("SELECT id FROM jobs WHERE source = :source AND source_job_id = :id")
            result = self.db.execute(query, {"source": source, "id": source_job_id}).fetchone()
            if result: return result[0]
        
        if content_hash:
            query = text("SELECT id FROM jobs WHERE content_hash = :hash")
            result = self.db.execute(query, {"hash": content_hash}).fetchone()
            if result: return result[0]
            
        return None

    def save_job(self, job: JobItem) -> int:
        # Use explicit params and prioritized standardized values
        params = {
            "source": job.source,
            "source_job_id": job.source_job_id,
            "title": job.title,
            "company_name": job.company_name,
            "location": job.std_location or job.location,
            "work_mode": job.std_work_mode or job.work_mode,
            "salary_text": job.salary_text,
            "annual_salary_min": job.annual_salary_min,
            "annual_salary_max": job.annual_salary_max,
            "salary_is_estimated": job.salary_is_estimated,
            "salary_note": job.salary_note,
            "jd_text": job.jd_text,
            "job_url": job.job_url,
            "content_hash": job.content_hash,
        }
        
        query = text("""
            INSERT INTO jobs (source, source_job_id, title, company_name, location, work_mode, 
                              salary_text, annual_salary_min, annual_salary_max, salary_is_estimated, 
                              salary_note, jd_text, job_url, content_hash, first_seen_at, 
                              last_seen_at, is_active)
            OUTPUT INSERTED.id
            VALUES (:source, :source_job_id, :title, :company_name, :location, :work_mode,
                    :salary_text, :annual_salary_min, :annual_salary_max, :salary_is_estimated,
                    :salary_note, :jd_text, :job_url, :content_hash, SYSUTCDATETIME(), SYSUTCDATETIME(), 1)
        """)
        result = self.db.execute(query, params).fetchone()
        self.db.commit()
        return result[0]

    def save_interview_guide(self, guide: InterviewGuide):
        query = text("""
            INSERT INTO interview_guides (job_id, jd_summary, resume_focus, required_skills, 
                                         bonus_skills, company_market_analysis, mock_questions, 
                                         portfolio_suggestions, risk_warnings, generated_by, created_at)
            VALUES (:job_id, :jd_summary, :resume_focus, :required_skills, :bonus_skills,
                    :company_market_analysis, :mock_questions, :portfolio_suggestions,
                    :risk_warnings, :generated_by, SYSUTCDATETIME())
        """)
        params = {
            "job_id": guide.job_id,
            "jd_summary": guide.jd_summary,
            "resume_focus": "\n".join(guide.resume_focus),
            "required_skills": "\n".join(guide.required_skills),
            "bonus_skills": "\n".join(guide.bonus_skills),
            "company_market_analysis": guide.company_market_analysis,
            "mock_questions": json.dumps(guide.mock_questions, ensure_ascii=False),
            "portfolio_suggestions": "\n".join(guide.portfolio_suggestions),
            "risk_warnings": "\n".join(guide.risk_warnings),
            "generated_by": guide.generated_by
        }
        self.db.execute(query, params)
        self.db.commit()
