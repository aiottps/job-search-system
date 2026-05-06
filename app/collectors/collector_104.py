from app.collectors.base import BaseCollector
from typing import List, Dict, Any
from app.collectors.playwright_utils import PlaywrightBrowser, random_delay, detect_blocking_or_login, safe_text, safe_attr
from app.utils.logger import logger
from app.config import config
import urllib.parse

class Collector104(BaseCollector):
    def search(self, keywords: List[str], locations: List[str]) -> List[Dict[str, Any]]:
        """Mock search for testing."""
        return [
            {
                "source": "104",
                "source_job_id": "104_mock_001",
                "title": "Python Developer",
                "company_name": "104 測試公司",
                "location": "台北市",
                "salary_text": "月薪 60,000 - 90,000",
                "job_url": "https://www.104.com.tw/job/mock001",
                "jd_text": "Python 開發經驗，熟悉 Web 框架。遠端面試。"
            }
        ]

    async def search_real(self, keywords: List[str], locations: List[str], max_results: int = 3) -> List[Dict[str, Any]]:
        """Real collector skeleton for 104."""
        logger.info(f"Starting 104 real search for {keywords}")
        
        # Build search URL (Simplified example)
        kw_str = " ".join(keywords)
        search_url = f"https://www.104.com.tw/jobs/search/?keyword={urllib.parse.quote(kw_str)}"
        
        jobs = []
        try:
            async with PlaywrightBrowser(headless=config.PLAYWRIGHT_HEADLESS, timeout=config.COLLECTOR_TIMEOUT_MS) as context:
                page = await context.new_page()
                await page.goto(search_url)
                await random_delay()

                # Detect blocking
                blocking = await detect_blocking_or_login(page)
                if blocking:
                    logger.warning(f"104 search blocked: {blocking}")
                    return []

                # Find job items (Using representative selectors)
                # NOTE: These selectors are examples and may need adjustment
                job_elements = await page.locator("article.job-list-item").all()
                
                for el in job_elements[:max_results]:
                    title_el = el.locator("a.js-job-link")
                    company_el = el.locator("ul.b-list-inline a") # Simplified
                    
                    job_url = await safe_attr(title_el, "href")
                    if job_url and job_url.startswith("//"):
                        job_url = "https:" + job_url

                    job = {
                        "source": "104",
                        "source_job_id": None, # Extract from URL if possible
                        "title": await safe_text(title_el),
                        "company_name": await safe_text(company_el),
                        "location": await safe_text(el.locator(".job-list-intro li:nth-child(1)")),
                        "salary_text": await safe_text(el.locator(".job-list-tag span:nth-child(1)")),
                        "job_url": job_url or "https://www.104.com.tw",
                        "jd_text": "資料不足 (詳情需進入詳細頁)"
                    }
                    
                    if job["title"] and job["company_name"]:
                        jobs.append(job)

        except Exception as e:
            logger.error(f"104 real search failed: {e}")
            
        return jobs

    def get_jd(self, job_url: str) -> str:
        return "104 Job Description Mock"
