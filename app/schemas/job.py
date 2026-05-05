from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict
from datetime import datetime

class JobItem(BaseModel):
    source: str
    source_job_id: Optional[str] = None
    title: str
    company_name: str
    location: Optional[str] = None
    work_mode: Optional[str] = "unknown"
    salary_text: Optional[str] = None
    annual_salary_min: Optional[int] = None
    annual_salary_max: Optional[int] = None
    salary_is_estimated: bool = False
    salary_note: Optional[str] = None
    jd_text: Optional[str] = None
    job_url: str
    content_hash: Optional[str] = None
    
    # Standardized fields (can be updated by normalizers)
    std_location: Optional[str] = None
    std_work_mode: Optional[str] = None

class CandidateProfile(BaseModel):
    preferred_name: Optional[str] = None
    gender_identity: Optional[str] = "prefer_not_to_say" # male, female, non_binary, prefer_not_to_say, self_describe
    accessibility_needs: List[str] = Field(default_factory=list) # sign_language_interpreter, live_caption, written_interview_questions, etc.
    communication_preferences: List[str] = Field(default_factory=list) # written_summary, slower_speaking_pace, camera_optional
    notes: Optional[str] = None

class InterviewSupportPlan(BaseModel):
    inclusive_interview_notes: List[str]
    accessibility_accommodation_checklist: List[str]
    jd_based_resume_optimization: List[str]
    jd_based_interview_focus: List[str]
    company_analysis: Dict
    risk_warnings: List[str]
    missing_information: List[str]

class CompanySource(BaseModel):
    source_name: str
    source_url: Optional[str] = None
    source_type: str # official, esg_report, government, news, job_platform, employee_review, forum, etc.
    published_at: Optional[str] = None
    content: str
    reliability_level: str # high, medium, low

class InclusionCategoryAnalysis(BaseModel):
    summary: str
    positive_signals: List[str] = Field(default_factory=list)
    risk_signals: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    sources: List[CompanySource] = Field(default_factory=list)

class CompanyInclusionAnalysis(BaseModel):
    company_name: str
    overall_summary: str
    gender_inclusion: InclusionCategoryAnalysis
    accessibility_support: InclusionCategoryAnalysis
    workplace_safety_and_fairness: InclusionCategoryAnalysis
    interview_questions_to_confirm: List[str] = Field(default_factory=list)
    evidence_limitations: List[str] = Field(default_factory=list)

class InterviewGuide(BaseModel):
    job_id: int
    jd_summary: str
    resume_focus: List[str]
    required_skills: List[str]
    bonus_skills: List[str]
    company_market_analysis: str
    mock_questions: List[dict]
    portfolio_suggestions: List[str]
    risk_warnings: List[str]
    generated_by: str = "Gemini"
