from google import genai
from app.config import config
import json
from pydantic import BaseModel
from typing import List, Dict

class JDAnalysis(BaseModel):
    jd_summary: str
    resume_focus: List[str]
    required_skills: List[str]
    bonus_skills: List[str]
    company_market_analysis: str
    mock_questions: List[Dict[str, str]]
    portfolio_suggestions: List[str]
    risk_warnings: List[str]
    missing_information: List[str]

def get_default_analysis() -> Dict:
    return {
        "jd_summary": "資料不足，無法產生摘要",
        "resume_focus": ["請根據職位需求調整履歷"],
        "required_skills": ["資料不足"],
        "bonus_skills": [],
        "company_market_analysis": "資料不足",
        "mock_questions": [{"question": "請介紹你自己", "intent": "基本了解", "suggested_answer_direction": "著重在與此職位相關的經驗"}],
        "portfolio_suggestions": ["資料不足"],
        "risk_warnings": ["資料不足，請人工確認職缺內容"],
        "missing_information": ["JD 內容過於簡略"]
    }

class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        self.model_id = "gemini-2.0-flash"

    def analyze_jd(self, jd_text: str, user_preferences: str) -> dict:
        if not jd_text or len(jd_text.strip()) < 10:
            return get_default_analysis()

        prompt = f"""
你是求職者的職涯陪跑教練。
請根據以下 JD 與使用者條件進行分析。
不得創造不存在的公司評價、面試經驗、薪資、福利或市場資訊。
如果資料不足，請明確標示「資料不足」。
請使用繁體中文為主，必要技術名詞可保留英文。
輸出必須符合 JSON schema。

使用者條件:
{user_preferences}

JD 內容:
{jd_text}
"""
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': JDAnalysis
                }
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return get_default_analysis()
