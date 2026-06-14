from typing import Dict, Any, List

class InterviewGameService:
    def get_challenges(self, job_id: str) -> Dict[str, Any]:
        if "data-engineer" in job_id:
            challenges = [
                {
                    "question": "請說明你在通天河數據如何降低 50% 的資料延遲？",
                    "why_it_matters": "面試官想確認你的實戰經驗與解決問題的邏輯。",
                    "answer_hint": "從瓶頸診斷、工具選擇、實施過程到最後的數據對比來回答。",
                    "confidence_boost": "這正是你的招牌法寶，儘管展現！",
                    "citation_id": "resume-01"
                },
                {
                    "question": "如果 SQL 筋斗雲突然卡住了（查詢變慢），你會如何診斷？",
                    "why_it_matters": "考察你對資料庫效能監控與優化的理解。",
                    "answer_hint": "提到查看 Execution Plan, Index 狀態以及鎖競爭等面向。",
                    "confidence_boost": "你對 SQL 有深厚研究，這題難不倒你。",
                    "citation_id": "resume-01"
                },
                {
                    "question": "如何確保資料取經之路的穩定性（Data Quality）？",
                    "why_it_matters": "在大數據環境下，資料的準確性至關重要。",
                    "answer_hint": "提到 Schema Validation, Unit Testing for ETL 以及監控報警。",
                    "confidence_boost": "展現你對資料工程嚴謹性的堅持。",
                    "citation_id": "job-demo-data-engineer"
                }
            ]
            monster = "追問妖"
            stage_name = "靈山數據中心試煉"
        else:
            challenges = [
                {
                    "question": "如何將一個枯燥的表單變成一個有趣的互動故事？",
                    "why_it_matters": "確認你對創意應用與使用者體驗的獨到見解。",
                    "answer_hint": "提到微互動、進度條視覺化、以及情境引導。",
                    "confidence_boost": "發揮你的想像力，這正是你的舞台。",
                    "citation_id": "job-demo-creative-app-dev"
                }
            ]
            monster = "枯燥魔"
            stage_name = "花果山創意工坊試煉"

        return {
            "stage_name": stage_name,
            "monster": monster,
            "opening_line": f"挑戰者，歡迎來到 {stage_name}！我是 {monster}，準備好接受我的試煉了嗎？",
            "challenges": challenges
        }
