from app.collectors.base import BaseCollector
from typing import List, Dict, Any
from app.collectors.playwright_utils import PlaywrightBrowser, random_delay, detect_blocking_or_login, safe_text, safe_attr
from app.utils.logger import logger
from app.config import config
import urllib.parse

class Collector1111(BaseCollector):
    def search(self, keywords: List[str], locations: List[str]) -> List[Dict[str, Any]]:
        """[MOCK] Search for verification purposes."""
        return [
            {
                "source": "1111",
                "source_job_id": "1111_verification_001",
                "title": "Data Engineer (大數據工程師)",
                "company_name": "桃園領先科技",
                "location": "桃園市中壢區",
                "salary_text": "年薪 800,000 - 1,200,000",
                "job_url": "https://www.1111.com.tw/job/verify1",
                "jd_text": "負責大數據平台建置與 ETL 流程開發。熟悉 SQL 與 Python。此職位需進辦公室。"
            },
            {
                "source": "1111",
                "source_job_id": "1111_verification_002",
                "title": "Senior Data Engineer",
                "company_name": "全球遠端數據公司",
                "location": "遠端",
                "salary_text": "月薪 70,000 - 100,000",
                "job_url": "https://www.1111.com.tw/job/verify2",
                "jd_text": "完全遠端辦公。建立雲端資料流水線。熟悉 Spark 與 Airflow。"
            }
        ]

    async def search_real(self, keywords: List[str], locations: List[str], max_results: int = 3) -> List[Dict[str, Any]]:
        """Real collector skeleton for 1111."""
        logger.info(f"Starting 1111 real search for {keywords}")
        
        # Build search URL (Simplified)
        kw_str = " ".join(keywords)
        search_url = f"https://www.1111.com.tw/search/job?ks={urllib.parse.quote(kw_str)}"
        
        jobs = []
        try:
            async with PlaywrightBrowser(headless=config.PLAYWRIGHT_HEADLESS, timeout=config.COLLECTOR_TIMEOUT_MS) as context:
                page = await context.new_page()
                await page.goto(search_url)
                await random_delay()

                # Detect blocking
                blocking = await detect_blocking_or_login(page)
                if blocking:
                    logger.warning(f"1111 search blocked: {blocking}")
                    return []

                # Find job items (Using representative selectors)
                # NOTE: These selectors are examples and may need adjustment
                job_elements = await page.locator(".job_item").all()
                
                for el in job_elements[:max_results]:
                    title_el = el.locator("h1 a, h2 a")
                    company_el = el.locator(".job_item_company")
                    
                    job_url = await safe_attr(title_el, "href")
                    if job_url and job_url.startswith("/"):
                        job_url = "https://www.1111.com.tw" + job_url

                    job = {
                        "source": "1111",
                        "source_job_id": None,
                        "title": await safe_text(title_el),
                        "company_name": await safe_text(company_el),
                        "location": await safe_text(el.locator(".job_item_info .item_info_txt").first),
                        "salary_text": await safe_text(el.locator(".job_item_info .item_info_salary")),
                        "job_url": job_url or "https://www.1111.com.tw",
                        "jd_text": "資料不足 (詳情需進入詳細頁)"
                    }
                    
                    if job["title"] and job["company_name"]:
                        jobs.append(job)

        except Exception as e:
            logger.error(f"1111 real search failed: {e}")
            
        return jobs

    def get_jd(self, job_url: str) -> str:
        return "1111 Job Description Mock"
