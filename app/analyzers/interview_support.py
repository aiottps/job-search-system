from typing import List, Dict, Optional
from app.schemas.job import JobItem, CandidateProfile, InterviewSupportPlan

def build_interview_support_plan(
    job: JobItem,
    candidate: CandidateProfile,
    company_sources: Optional[List[Dict]] = None
) -> InterviewSupportPlan:
    """
    Builds an inclusive interview support plan based on the JD and candidate profile.
    Ensures non-discrimination and data-driven suggestions.
    """
    
    # 1. JD-based Resume Optimization
    resume_optimization = []
    jd_lower = (job.jd_text or "").lower()
    
    if any(k in jd_lower for k in ["python", "etl", "sql"]):
        resume_optimization.append("履歷建議強調 Python、SQL 與 ETL 相關專案經驗與成果。")
    if any(k in jd_lower for k in ["spark", "airflow", "cloud", "雲端"]):
        resume_optimization.append("履歷建議強調資料管線 (Data Pipeline)、排程監控 (Airflow) 與雲端平台開發經驗。")
    if not resume_optimization:
        resume_optimization.append("根據 JD 關鍵字調整履歷中對應的技術棧描述。")

    # 2. JD-based Interview Focus
    interview_focus = []
    if "python" in jd_lower:
        interview_focus.append("面試準備：著重 Python 演算法、資料處理邏輯與非同步編程（若適用）。")
    if "sql" in jd_lower:
        interview_focus.append("面試準備：熟悉資料庫索引優化、複雜 JOIN 查詢與視圖設計。")
    if not interview_focus:
        interview_focus.append("面試準備：著重 JD 中提及的核心職能與軟實力要求。")

    # 3. Inclusive Interview Notes & Accessibility
    inclusive_notes = []
    accommodation_checklist = []
    
    if candidate.preferred_name:
        inclusive_notes.append(f"面試溝通建議：使用使用者自願提供的稱謂 '{candidate.preferred_name}'。")

    if "sign_language_interpreter" in candidate.accessibility_needs:
        accommodation_checklist.append("面試前應主動向 HR 確認是否可安排手語翻譯人員。")
        accommodation_checklist.append("確認面試過程是否可提供書面題目或會後文字摘要。")
        accommodation_checklist.append("確認視訊工具是否支援字幕或即時文字聊天功能。")
        accommodation_checklist.append("確認是否需要延長作答時間或改採書面方式補充回答。")

    if "wheelchair_access" in candidate.accessibility_needs:
        accommodation_checklist.append("確認面試場地具備無障礙空間與設施。")

    # 4. Company Analysis (Strictly data-driven)
    company_analysis = {"summary": "資料不足", "details": []}
    if company_sources:
        # Simplified for mock logic
        company_analysis["summary"] = f"根據提供之 {len(company_sources)} 筆來源進行分析。"
        company_analysis["details"] = company_sources
    
    # 5. Risk Warnings & Missing Information
    risk_warnings = []
    missing_info = []
    
    if not job.salary_text or job.salary_text == "面議":
        risk_warnings.append("薪資範圍未明確標示。")
    if not job.work_mode or job.work_mode == "unknown":
        risk_warnings.append("遠端/混合辦公政策未明確標示。")
    if not job.jd_text or len(job.jd_text) < 50:
        missing_info.append("JD 內容過於簡略，難以產生具體職能建議。")
    if not company_sources:
        missing_info.append("公司公開背景資料不足。")

    return InterviewSupportPlan(
        inclusive_interview_notes=inclusive_notes,
        accessibility_accommodation_checklist=accommodation_checklist,
        jd_based_resume_optimization=resume_optimization,
        jd_based_interview_focus=interview_focus,
        company_analysis=company_analysis,
        risk_warnings=risk_warnings,
        missing_information=missing_info
    )
