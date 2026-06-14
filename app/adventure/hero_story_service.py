from typing import Dict, Any, List
from app.iq.grounded_context_service import GroundedContextService
import json

class HeroStoryService:
    def generate_story(self, iq_service: GroundedContextService, job_id: str) -> Dict[str, Any]:
        profile_ctx = iq_service.get_context_by_type("candidate_profile")
        job_ctx = iq_service.get_context_by_id(f"job-{job_id}")
        
        if not profile_ctx or not job_ctx:
            return {"hero_title": "冒險故事", "journey_story": "資料不足"}

        profile = json.loads(profile_ctx[0]["content"])
        job = json.loads(job_ctx["content"])

        return {
            "hero_title": f"{profile['name']} 的西天取經路",
            "opening": f"在資料的汪洋大海中，有一位名為 {profile['name']} 的修行者，手握 Python 金箍棒，正尋找著屬於他的真經。",
            "journey_story": f"前方出現了一座名為 {job['company_name']} 的巍峨大山。這不是一座平凡的山，而是通往 {job['title']} 境界的必經之路。雖然路途充滿挑戰，但 {profile['name']} 已經在通天河數據與盤絲洞科技累積了深厚的內功。",
            "three_magic_tools": [
                "Python 金箍棒 (自動化開發)",
                "SQL 筋斗雲 (數據優化)",
                "問題拆解照妖鏡 (系統分析)"
            ],
            "turning_point": "當他在面對海量資料的挑戰時，他想起了過往成功降低延遲的經驗，心中湧現了無比的勇氣。",
            "next_chapter": f"現在，他正準備叩響 {job['company_name']} 的大門，開啟全新的修行篇章。",
            "citations": [profile_ctx[0], job_ctx]
        }
