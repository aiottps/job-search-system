import pytest
import os
from app.iq.grounded_context_service import GroundedContextService

def test_context_loading():
    # Ensure demo files exist
    assert os.path.exists("demo_data/candidate_profile.json")
    
    service = GroundedContextService(demo_data_dir="demo_data")
    contexts = service.get_all_contexts()
    
    assert len(contexts) >= 4 # profile, resume, 2 jobs, company
    
    resume = service.get_context_by_type("resume")
    assert len(resume) == 1
    assert "張小凡" in resume[0]["content"]
