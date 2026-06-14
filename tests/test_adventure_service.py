import pytest
from app.iq.grounded_context_service import GroundedContextService
from app.adventure.adventure_service import AdventureService

def test_adventure_generation():
    iq_service = GroundedContextService(demo_data_dir="demo_data")
    adventure_service = AdventureService(iq_service)
    
    res = adventure_service.generate_adventure("demo-data-engineer")
    
    assert "candidate_strengths" in res
    assert "job_bright_spots" in res
    assert "hero_story" in res
    assert "quest_scroll" in res
    assert "interview_game" in res
    assert "citations" in res
    assert len(res["citations"]) > 0

def test_adventure_data_insufficient():
    iq_service = GroundedContextService(demo_data_dir="demo_data")
    adventure_service = AdventureService(iq_service)
    
    # Try with non-existent job
    res = adventure_service.generate_adventure("non-existent")
    assert res["hero_story"]["journey_story"] == "資料不足"
