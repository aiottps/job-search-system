from app.collectors.base import BaseCollector
from typing import List, Dict, Any

class Collector104(BaseCollector):
    def search(self, keywords: List[str], locations: List[str]) -> List[Dict[str, Any]]:
        print(f"Searching 104 for {keywords} in {locations}...")
        # Mock results for now
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

    def get_jd(self, job_url: str) -> str:
        # TODO: Implement Playwright logic for real crawling
        return "104 Job Description Mock"
