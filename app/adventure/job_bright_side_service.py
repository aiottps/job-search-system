from typing import Dict, Any, List
from app.iq.grounded_context_service import GroundedContextService
import json

class JobBrightSideService:
    def get_bright_spots(self, iq_service: GroundedContextService, job_id: str) -> Dict[str, Any]:
        job_ctx = iq_service.get_context_by_id(f"job-{job_id}")
        if not job_ctx:
            return {"title": "這座山門值得一闖的原因", "bright_spots": [], "encouragement": "資料不足"}

        job_data = json.loads(job_ctx["content"])
        
        # Simulate bright spots extraction
        bright_spots = [
            {
                "name": "雲端修行環境",
                "description": f"職缺地點位於 {job_data['location']}，讓你能在任何角落靜心修煉。",
                "why_it_matters": "節省通勤時間，能有更多精力精進技術。",
                "citation_id": f"job-{job_id}"
            },
            {
                "name": "豐厚修行資源",
                "description": f"提供 {job_data['salary_text']} 的俸祿，支撐你的修行之路。",
                "why_it_matters": "穩定的經濟來源是長期修行的基石。",
                "citation_id": f"job-{job_id}"
            },
            {
                "name": "各方大能共事",
                "description": "團隊重視程式碼品質與協作，你將與各路高手一同闖關。",
                "why_it_matters": "良好的團隊氛圍能讓你進步神速。",
                "citation_id": f"job-{job_id}"
            }
        ]

        return {
            "title": "這座山門值得一闖的原因",
            "bright_spots": bright_spots,
            "encouragement": f"這座 {job_data['company_name']} 的山門，正等待著如你一般的有緣人。"
        }
