from app.collectors.base import BaseCollector
from typing import List, Dict, Any

class LinkedInManual(BaseCollector):
    """
    LinkedIn collector for manual job description input.
    Automated scraping is strictly prohibited.
    """
    def search(self, keywords: List[str], locations: List[str]) -> List[Dict[str, Any]]:
        # LinkedIn automated search is not implemented.
        # This can be used to process manually added URLs/IDs.
        return []

    def get_jd(self, job_url: str) -> str:
        # User is expected to provide the JD text manually for LinkedIn.
        return "LinkedIn Job Description (Manual Import Required)"

    def process_manual_input(self, title: str, company: str, jd_text: str, url: str) -> Dict[str, Any]:
        """Helper to format manual input into the standard contract."""
        return {
            "source": "LinkedIn_Manual",
            "source_job_id": None,
            "title": title,
            "company_name": company,
            "location": "unknown",
            "salary_text": "面議",
            "job_url": url,
            "jd_text": jd_text
        }
