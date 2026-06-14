from typing import Dict, Any, List

class QuestService:
    def get_quests(self, job_id: str) -> Dict[str, Any]:
        # Simulate quest generation based on job type
        if "data-engineer" in job_id:
            quests = [
                {
                    "level": 1,
                    "mission": "複習 Spark 優化心法",
                    "deliverable": "整理一份關於 Join 策略的筆記",
                    "confidence_boost": "增強對大數據處理的掌控感",
                    "estimated_time": "30 分鐘"
                },
                {
                    "level": 2,
                    "mission": "模擬 SQL 效能瓶頸分析",
                    "deliverable": "寫出三個優化慢查詢的策略",
                    "confidence_boost": "展現解決真實問題的能力",
                    "estimated_time": "45 分鐘"
                },
                {
                    "level": 3,
                    "mission": "準備通天河數據的案例分享",
                    "deliverable": "準備 3 分鐘的成功案例講稿",
                    "confidence_boost": "強化面試時的論據支撐",
                    "estimated_time": "60 分鐘"
                }
            ]
        else:
            quests = [
                {
                    "level": 1,
                    "mission": "收集創意 Web 應用的靈感",
                    "deliverable": "建立一個包含 5 個優秀 UI 案例的清單",
                    "confidence_boost": "提升對美感的敏銳度",
                    "estimated_time": "30 分鐘"
                },
                {
                    "level": 2,
                    "mission": "複習 FastAPI 非同步心法",
                    "deliverable": "寫一段簡單的 async endpoint 範例",
                    "confidence_boost": "確保技術基本功穩固",
                    "estimated_time": "40 分鐘"
                }
            ]

        return {
            "quest_title": "下一關任務卷軸",
            "quests": quests,
            "final_boss": {
                "mission": "叩響山門（投遞履歷）",
                "demo_line": "我已準備就緒，請開啟面試試煉！"
            }
        }
