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
        [MOCK] Search for jobs using static/mock data for testing.
        """
        pass

    async def search_real(self, keywords: List[str], locations: List[str], max_results: int = 3) -> List[Dict[str, Any]]:
        """
        [REAL] Perform actual web scraping using Playwright.
        
        Constraints:
        - Only access public search pages.
        - DO NOT log in.
        - DO NOT bypass CAPTCHAs.
        - Max results per call is capped.
        """
        return []

    @abstractmethod
    def get_jd(self, job_url: str) -> str:
        """Fetch the full Job Description text from a job URL."""
        pass
