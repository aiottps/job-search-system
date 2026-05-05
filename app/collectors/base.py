from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseCollector(ABC):
    """
    Base class for all job collectors.
    
    IMPORTANT: 
    - Collectors MUST return a list of dictionaries compatible with JobItem.
    - Automated login or scraping of LinkedIn is strictly prohibited.
    - Use public search pages or manual data injection for LinkedIn.
    """

    @abstractmethod
    def search(self, keywords: List[str], locations: List[str]) -> List[Dict[str, Any]]:
        """
        Search for jobs and return a list of raw job dictionaries.
        
        Expected fields in each dict:
            source, title, company_name, location, 
            salary_text, job_url, jd_text
        
        Optional field:
            source_job_id: Platform-specific ID. If missing, deduplication
                           will rely on content_hash.
        """
        pass

    @abstractmethod
    def get_jd(self, job_url: str) -> str:
        """Fetch the full Job Description text from a job URL."""
        pass
