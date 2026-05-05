import pytest
from app.schemas.job import CompanySource
from app.analyzers.company_inclusion import analyze_company_inclusion

def test_no_sources():
    """測試 1：沒有來源"""
    res = analyze_company_inclusion("測試公司", [])
    assert res.overall_summary == "資料不足"
    assert res.gender_inclusion.summary == "資料不足"
    assert res.accessibility_support.summary == "資料不足"
    assert res.workplace_safety_and_fairness.summary == "資料不足"
    assert any("沒有可用來源" in lim for lim in res.evidence_limitations)

def test_official_high_reliability():
    """測試 2：官方來源包含性別平等與反騷擾"""
    src = CompanySource(
        source_name="官方永續報告",
        source_type="official",
        reliability_level="high",
        content="本公司承諾性別平等，並設有完善的反騷擾與平等機會政策。"
    )
    res = analyze_company_inclusion("官方公司", [src])
    
    assert len(res.gender_inclusion.positive_signals) >= 2
    assert "性別平等" in res.gender_inclusion.positive_signals
    assert "反騷擾" in res.gender_inclusion.positive_signals
    # 確保沒有憑空產生無障礙訊號
    assert res.accessibility_support.summary == "資料不足"

def test_accessibility_signals():
    """測試 3：來源包含手語翻譯與字幕"""
    src = CompanySource(
        source_name="面試心得",
        source_type="interview_review",
        reliability_level="medium",
        content="面試時公司主動提供手語翻譯與即時字幕，並準備了書面題目。"
    )
    res = analyze_company_inclusion("友善公司", [src])
    
    pos = res.accessibility_support.positive_signals
    assert "手語翻譯" in pos
    assert "字幕" in pos
    assert "書面題目" in pos
    # 確保不把無障礙協助列為風險
    assert len(res.accessibility_support.risk_signals) == 0

def test_low_reliability_forum():
    """測試 4：低可靠匿名評論"""
    src = CompanySource(
        source_name="職場論壇",
        source_type="forum",
        reliability_level="low",
        content="這家公司有嚴重的職場霸凌問題，申訴無效。"
    )
    res = analyze_company_inclusion("霸凌公司", [src])
    
    assert "職場霸凌" in res.workplace_safety_and_fairness.risk_signals
    assert "申訴無效" in res.workplace_safety_and_fairness.risk_signals
    assert "低可靠來源" in res.overall_summary
    assert any("低可靠來源" in lim for lim in res.evidence_limitations)

def test_no_fabrication():
    """測試 5：不得捏造公司資訊"""
    # 只提供性別平等來源，不提供無障礙來源
    src = CompanySource(
        source_name="新聞",
        source_type="news",
        reliability_level="medium",
        content="該公司獲頒性別平等優良企業。"
    )
    res = analyze_company_inclusion("性平公司", [src])
    
    assert "性別平等" in res.gender_inclusion.positive_signals
    assert res.accessibility_support.summary == "資料不足"
    assert any("缺少公司對於無障礙" in lim for lim in res.evidence_limitations)

if __name__ == "__main__":
    pytest.main([__file__])
