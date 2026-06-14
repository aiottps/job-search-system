import pytest
from app.adventure.interview_game_service import InterviewGameService

def test_interview_challenges():
    service = InterviewGameService()
    
    challenges = service.get_challenges("demo-data-engineer")
    assert challenges["monster"] == "追問妖"
    assert len(challenges["challenges"]) >= 3
    
    challenges_creative = service.get_challenges("demo-creative-app-dev")
    assert challenges_creative["monster"] == "枯燥魔"
