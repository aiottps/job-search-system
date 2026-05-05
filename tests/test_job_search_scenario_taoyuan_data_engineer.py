import pytest
from app.collectors.collector_1111 import Collector1111
from app.schemas.job import JobItem
from app.normalizers.salary import parse_salary
from app.normalizers.location import normalize_location
from app.normalizers.work_mode import normalize_work_mode

def test_job_search_scenario_taoyuan_data_engineer():
    """
    Scenario Test:
    - Keywords: Data Engineer / 數據工程師
    - Locations: 桃園市, 遠端
    - Salary: >= 800,000
    - Logic: Mock Data -> JobItem -> Normalize -> Filter
    """
    collector = Collector1111()
    
    # 1. Fetch Mock Verification Data
    # The current Collector1111.search ignores inputs but we pass them for contract consistency
    raw_jobs = collector.search(["Data Engineer"], ["桃園市", "遠端"])
    
    processed_jobs = []
    
    # 2. Process and Normalize
    for raw in raw_jobs:
        job = JobItem(**raw)
        
        # Salary
        salary_res = parse_salary(job.salary_text)
        job.annual_salary_min = salary_res.annual_min
        job.annual_salary_max = salary_res.annual_max
        job.salary_is_estimated = salary_res.is_estimated
        job.salary_note = salary_res.note
        
        # Location
        job.std_location = normalize_location(job.location)
        
        # Work Mode
        job.std_work_mode = normalize_work_mode(job.jd_text, job.location)
        
        processed_jobs.append(job)

    # 3. Apply Filtering Logic (Matching our target criteria)
    keywords = ["data engineer", "數據工程師", "資料工程師", "大數據工程師"]
    
    def matches_criteria(job: JobItem):
        # Salary Check (>= 800,000)
        salary_match = job.annual_salary_min is not None and job.annual_salary_min >= 800000
        
        # Location Check (桃園市 or 遠端)
        location_match = job.std_location in ["桃園市", "遠端"]
        
        # Work Mode Check (onsite or remote)
        mode_match = job.std_work_mode in ["onsite", "remote"]
        
        # Content Check (Title or JD contains keywords)
        content_text = (job.title + " " + (job.jd_text or "")).lower()
        keyword_match = any(kw in content_text for kw in keywords)
        
        return salary_match and location_match and mode_match and keyword_match

    filtered_jobs = [j for j in processed_jobs if matches_criteria(j)]

    # 4. Assertions
    # We expect at least 2 jobs based on the current Collector1111 mock data
    assert len(filtered_jobs) >= 2, f"Expected at least 2 matches, found {len(filtered_jobs)}"
    
    # Granular Checks
    for job in filtered_jobs:
        assert job.annual_salary_min >= 800000, f"Salary too low: {job.annual_salary_min}"
        assert job.salary_is_estimated is False, f"Salary should not be estimated for {job.title}"

    # Verify specific cases
    taoyuan_onsite = next(j for j in filtered_jobs if j.std_location == "桃園市" and j.std_work_mode == "onsite")
    remote_remote = next(j for j in filtered_jobs if j.std_location == "遠端" and j.std_work_mode == "remote")
    
    assert taoyuan_onsite.annual_salary_min == 800000, f"Expected 800,000 for Taoyuan, got {taoyuan_onsite.annual_salary_min}"
    assert remote_remote.annual_salary_min == 840000, f"Expected 840,000 (70k*12) for Remote, got {remote_remote.annual_salary_min}"


if __name__ == "__main__":
    pytest.main([__file__])
