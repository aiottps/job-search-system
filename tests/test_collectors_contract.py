import pytest
from app.collectors.collector_104 import Collector104
from app.collectors.collector_1111 import Collector1111
from app.schemas.job import JobItem

def test_collectors_contract():
    collectors = [Collector104(), Collector1111()]
    
    # Required fields that cannot be empty
    required_fields = {
        "source", "title", "company_name", 
        "location", "salary_text", "job_url", "jd_text"
    }
    
    # source_job_id is optional

    for collector in collectors:
        results = collector.search(["Python"], ["台北市"])
        assert isinstance(results, list)
        
        for job_dict in results:
            # Check for required fields existence and non-emptiness
            for field in required_fields:
                assert field in job_dict, f"Missing field {field} in {collector.__class__.__name__}"
                val = job_dict[field]
                assert val is not None, f"Field {field} is None in {collector.__class__.__name__}"
                assert str(val).strip() != "", (
                    f"Field {field} is empty in {collector.__class__.__name__}"
                )
            
            # URL check
            url = job_dict["job_url"]
            assert url.startswith("http://") or url.startswith("https://"), (
                f"Invalid job_url format: {url}"
            )
            
            # Check if it can initialize a JobItem
            try:
                job_item = JobItem(**job_dict)
                assert job_item.title is not None
            except Exception as e:
                pytest.fail(f"Validation failed for {collector.__class__.__name__}: {e}")

if __name__ == "__main__":
    pytest.main([__file__])
