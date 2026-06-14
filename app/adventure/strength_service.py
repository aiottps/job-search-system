from typing import Dict, Any, List
from app.iq.grounded_context_service import GroundedContextService

class StrengthService:
    def get_strengths(self, iq_service: GroundedContextService) -> Dict[str, Any]:
        # In a real app, this would use LLM with grounded context
        # Here we simulate it by reading the resume context
        resume_ctx = iq_service.get_context_by_type("resume")
        if not resume_ctx:
            return {"title": "你身上的三件法寶", "strengths": [], "confidence_line": "資料不足，尚待修行"}

        # Simulate extraction
        return {
            "title": "你身上的三件法寶",
            "strengths": [
                {
                    "name": "Python 金箍棒",
                    "description": "具備深厚的 Python 開發本領，能隨心所欲地編寫自動化腳本與後端邏輯。",
                    "evidence": "修行履歷中提及熟練使用 Python 進行後端開發。",
                    "citation_id": "resume-01"
                },
                {
                    "name": "SQL 筋斗雲",
                    "description": "精通 SQL 查詢優化，能在大數據的海量訊息中快速翻騰，尋找關鍵真相。",
                    "evidence": "修行履歷中提及精通 SQL 查詢優化，並有 3 年經驗。",
                    "citation_id": "resume-01"
                },
                {
                    "name": "資料建構術",
                    "description": "擅長 ETL 流程設計，能將混亂的原始資料梳理成井然有序的知識寶庫。",
                    "evidence": "曾於通天河數據成功將資料延遲降低 50%。",
                    "citation_id": "resume-01"
                }
            ],
            "confidence_line": "少俠，你已有如此本領，足以應對前方的妖魔鬼怪！"
        }
