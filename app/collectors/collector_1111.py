from app.collectors.base import BaseCollector
from typing import List, Dict, Any

class Collector1111(BaseCollector):
    def search(self, keywords: List[str], locations: List[str]) -> List[Dict[str, Any]]:
        print(f"Searching 1111 for {keywords} in {locations}...")
        
        # NOTE: This data is for MOCK VERIFICATION only. 
        # Real scraping via Playwright is NOT yet implemented.
        # This allows verifying the pipeline logic with specific scenarios (e.g. Data Engineer, >800k, Taoyuan/Remote).
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

    def get_jd(self, job_url: str) -> str:
        # TODO: Implement Playwright logic for real crawling
        return "1111 Job Description Verification Content"
