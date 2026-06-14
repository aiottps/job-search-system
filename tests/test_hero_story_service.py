import pytest
from app.iq.grounded_context_service import GroundedContextService
from app.adventure.hero_story_service import HeroStoryService

def test_hero_story_content():
    iq_service = GroundedContextService(demo_data_dir="demo_data")
    service = HeroStoryService()
    
    story = service.generate_story(iq_service, "demo-data-engineer")
    
    assert "張小凡" in story["hero_title"]
    assert "金箍棒" in story["opening"]
    assert "靈山數據科技" in story["journey_story"]
