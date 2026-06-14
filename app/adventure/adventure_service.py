from typing import Dict, Any, List
from app.iq.grounded_context_service import GroundedContextService
from app.iq.citation_builder import CitationBuilder
from app.adventure.strength_service import StrengthService
from app.adventure.job_bright_side_service import JobBrightSideService
from app.adventure.hero_story_service import HeroStoryService
from app.adventure.quest_service import QuestService
from app.adventure.interview_game_service import InterviewGameService

class AdventureService:
    def __init__(self, iq_service: GroundedContextService):
        self.iq_service = iq_service
        self.strength_service = StrengthService()
        self.job_bright_side_service = JobBrightSideService()
        self.hero_story_service = HeroStoryService()
        self.quest_service = QuestService()
        self.interview_game_service = InterviewGameService()

    def generate_adventure(self, job_id: str) -> Dict[str, Any]:
        citation_builder = CitationBuilder()
        
        # 1. Strengths
        strengths = self.strength_service.get_strengths(self.iq_service)
        for s in strengths.get("strengths", []):
            citation_builder.add_citation(self.iq_service.get_context_by_id(s.get("citation_id")))

        # 2. Job Bright Spots
        bright_spots = self.job_bright_side_service.get_bright_spots(self.iq_service, job_id)
        for b in bright_spots.get("bright_spots", []):
            citation_builder.add_citation(self.iq_service.get_context_by_id(b.get("citation_id")))

        # 3. Hero Story
        story = self.hero_story_service.generate_story(self.iq_service, job_id)
        for c in story.get("citations", []):
            citation_builder.add_citation(c)

        # 4. Quests
        quests = self.quest_service.get_quests(job_id)

        # 5. Interview Game
        interview_game = self.interview_game_service.get_challenges(job_id)
        for c in interview_game.get("challenges", []):
            citation_builder.add_citation(self.iq_service.get_context_by_id(c.get("citation_id")))

        return {
            "candidate_strengths": strengths,
            "job_bright_spots": bright_spots,
            "hero_story": story,
            "quest_scroll": quests,
            "interview_game": interview_game,
            "application_pack": {
                "linkedin_intro": "你好，我是對資料工程充滿熱情的修行者張小凡...",
                "cover_letter_opening": "在看到靈山數據科技的山門時，我便知道這是我下一階段修行的最佳去處...",
                "elevator_pitch": "我有 3 年的資料修行經驗，擅長用 Python 金箍棒解決複雜的 ETL 難題...",
                "confidence_mantra": "焦慮是暫時的，真經是永恆的。我有本領，我有法寶，我能成功。"
            },
            "confidence_badges": [
                "Python 金箍棒",
                "SQL 筋斗雲",
                "問題拆解照妖鏡"
            ],
            "citations": citation_builder.get_citations()
        }
