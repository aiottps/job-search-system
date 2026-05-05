import pytest
from app.schemas.job import JobItem, CandidateProfile
from app.analyzers.interview_support import build_interview_support_plan

@pytest.fixture
def data_engineer_job():
    return JobItem(
        source="1111",
        title="Data Engineer",
        company_name="測試科技",
        location="桃園市",
        salary_text="年薪 80萬 - 120萬",
        jd_text="負責 Python ETL 開發，熟悉 SQL 數據庫優化。具備 Spark 經驗者佳。",
        job_url="https://example.com/job"
    )

def test_gender_neutrality(data_engineer_job):
    """測試 1: 不同性別偏好但在相同職缺下，專業建議應完全一致。"""
    male_candidate = CandidateProfile(gender_identity="male", preferred_name="小明")
    female_candidate = CandidateProfile(gender_identity="female", preferred_name="小華")
    
    plan_male = build_interview_support_plan(data_engineer_job, male_candidate)
    plan_female = build_interview_support_plan(data_engineer_job, female_candidate)
    
    assert plan_male.jd_based_resume_optimization == plan_female.jd_based_resume_optimization
    assert plan_male.jd_based_interview_focus == plan_female.jd_based_interview_focus
    assert "小明" in plan_male.inclusive_interview_notes[0]
    assert "小華" in plan_female.inclusive_interview_notes[0]

def test_sign_language_accessibility(data_engineer_job):
    """測試 2: 手語翻譯支援需求應轉化為具體查核清單，且不得視為負面風險。"""
    candidate = CandidateProfile(
        accessibility_needs=["sign_language_interpreter"]
    )
    
    plan = build_interview_support_plan(data_engineer_job, candidate)
    
    checklist = "\n".join(plan.accessibility_accommodation_checklist)
    assert "手語翻譯" in checklist
    assert "書面題目" in checklist or "文字摘要" in checklist
    assert "字幕" in checklist or "文字聊天" in checklist
    
    # 確保風險提醒不包含歧視性內容，且不把手語協助列入
    for risk in plan.risk_warnings:
        assert "手語" not in risk
        assert "翻譯" not in risk

def test_data_driven_company_analysis(data_engineer_job):
    """測試 3: 無來源時公司分析應標示資料不足，不得捏造。"""
    candidate = CandidateProfile()
    
    # 案例：無來源資料
    plan_no_source = build_interview_support_plan(data_engineer_job, candidate, company_sources=[])
    assert plan_no_source.company_analysis["summary"] == "資料不足"
    
    # 案例：有來源資料
    sources = [{"source_name": "新聞", "content": "該公司最近獲得融資。"}]
    plan_with_source = build_interview_support_plan(data_engineer_job, candidate, company_sources=sources)
    assert "1 筆來源" in plan_with_source.company_analysis["summary"]

def test_jd_keyword_optimization(data_engineer_job):
    """測試 4: 履歷與面試建議應準確命中 JD 關鍵字。"""
    candidate = CandidateProfile()
    plan = build_interview_support_plan(data_engineer_job, candidate)
    
    resume_text = "\n".join(plan.jd_based_resume_optimization)
    assert any(k in resume_text for k in ["Python", "SQL", "ETL"])
    assert "Spark" in resume_text or "Data Pipeline" in resume_text
    
    interview_text = "\n".join(plan.jd_based_interview_focus)
    assert "Python" in interview_text
    assert "SQL" in interview_text

if __name__ == "__main__":
    pytest.main([__file__])
