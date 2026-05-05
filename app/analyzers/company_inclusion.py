from typing import List, Dict, Optional
from app.schemas.job import (
    CompanySource, 
    InclusionCategoryAnalysis, 
    CompanyInclusionAnalysis
)

def analyze_company_inclusion(
    company_name: str, 
    sources: List[CompanySource]
) -> CompanyInclusionAnalysis:
    """
    Analyzes company inclusion and accessibility signals based on provided sources.
    Strictly follows data-driven logic without fabrication.
    """
    
    # 1. Handle Empty Sources
    if not sources:
        insufficient = "資料不足"
        return CompanyInclusionAnalysis(
            company_name=company_name,
            overall_summary=insufficient,
            gender_inclusion=InclusionCategoryAnalysis(summary=insufficient),
            accessibility_support=InclusionCategoryAnalysis(summary=insufficient),
            workplace_safety_and_fairness=InclusionCategoryAnalysis(summary=insufficient),
            interview_questions_to_confirm=[
                "公司是否有正式的反歧視與反騷擾政策？",
                "面試若需要手語翻譯、字幕或書面題目，是否可以提前安排？",
                "若需要無障礙面試場地或遠端面試，公司是否可協助？",
                "公司是否有正式申訴或員工協助管道？"
            ],
            evidence_limitations=["目前沒有可用來源，無法判斷公司包容性與無障礙支援情況。"]
        )

    # 2. Define Keyword Maps
    GENDER_POS = ["性別平等", "多元共融", "dei", "反歧視", "反騷擾", "育嬰", "照護假", "平等機會", "女性主管", "員工資源團體"]
    GENDER_RISK = ["性騷擾", "性別歧視", "同工不同酬", "不當面試問題", "懷孕歧視", "育嬰歧視"]
    
    ACC_POS = ["無障礙空間", "手語翻譯", "字幕", "書面題目", "輔具", "遠端面試", "彈性溝通", "合理調整", "accessibility", "accommodation"]
    ACC_RISK = ["拒絕合理調整", "無障礙不足", "不提供協助", "歧視身心障礙", "無法提供字幕", "不接受手語翻譯"]
    
    SAFETY_POS = ["申訴制度", "吹哨者保護", "勞資溝通", "反霸凌", "心理安全", "職場安全"]
    SAFETY_RISK = ["職場霸凌", "違法加班", "勞資爭議", "不當解僱", "欠薪", "高壓管理", "申訴無效"]

    def extract_signals(content: str, keywords: List[str]) -> List[str]:
        found = []
        content_lower = content.lower()
        for kw in keywords:
            if kw.lower() in content_lower:
                found.append(kw)
        return found

    # 3. Categorize Sources and Signals
    gender_analysis = {"pos": [], "risk": [], "srcs": []}
    acc_analysis = {"pos": [], "risk": [], "srcs": []}
    safety_analysis = {"pos": [], "risk": [], "srcs": []}
    
    has_low_reliability = False
    
    for src in sources:
        if src.reliability_level == "low":
            has_low_reliability = True
            
        # Gender
        gp = extract_signals(src.content, GENDER_POS)
        gr = extract_signals(src.content, GENDER_RISK)
        if gp or gr:
            gender_analysis["pos"].extend(gp)
            gender_analysis["risk"].extend(gr)
            gender_analysis["srcs"].append(src)
            
        # Accessibility
        ap = extract_signals(src.content, ACC_POS)
        ar = extract_signals(src.content, ACC_RISK)
        if ap or ar:
            acc_analysis["pos"].extend(ap)
            acc_analysis["risk"].extend(ar)
            acc_analysis["srcs"].append(src)
            
        # Safety
        sp = extract_signals(src.content, SAFETY_POS)
        sr = extract_signals(src.content, SAFETY_RISK)
        if sp or sr:
            safety_analysis["pos"].extend(sp)
            safety_analysis["risk"].extend(sr)
            safety_analysis["srcs"].append(src)

    # 4. Finalize Category Summaries
    def build_category(name: str, data: Dict) -> InclusionCategoryAnalysis:
        pos = sorted(list(set(data["pos"])))
        risk = sorted(list(set(data["risk"])))
        srcs = data["srcs"]
        
        if not pos and not risk:
            return InclusionCategoryAnalysis(summary="資料不足", missing_information=[f"缺少關於{name}的具體實踐或評價來源。"])
        
        summary_text = ""
        if pos:
            summary_text += f"發現 {len(pos)} 項正向訊號。 "
        if risk:
            summary_text += f"發現 {len(risk)} 項需留意之風險訊號。 "
            
        # Reliability warning
        if any(s.reliability_level == "low" for s in srcs):
            summary_text += "（包含低可靠來源，請審慎判斷）"
            
        return InclusionCategoryAnalysis(
            summary=summary_text.strip(),
            positive_signals=pos,
            risk_signals=risk,
            sources=srcs
        )

    gender_cat = build_category("性別包容性", gender_analysis)
    acc_cat = build_category("無障礙支援", acc_analysis)
    safety_cat = build_category("職場公平與安全", safety_analysis)

    # 5. Overall Summary
    overall = "根據目前可用來源，"
    if not any([gender_cat.positive_signals, gender_cat.risk_signals, 
                acc_cat.positive_signals, acc_cat.risk_signals,
                safety_cat.positive_signals, safety_cat.risk_signals]):
        overall = "資料不足"
    else:
        signals_count = len(gender_cat.positive_signals) + len(acc_cat.positive_signals) + len(safety_cat.positive_signals)
        risks_count = len(gender_cat.risk_signals) + len(acc_cat.risk_signals) + len(safety_cat.risk_signals)
        overall += f"共識別出 {signals_count} 項正向訊號與 {risks_count} 項風險訊號。"
        if has_low_reliability:
            overall += " 注意：部分資訊來自低可靠來源。"

    limitations = []
    if has_low_reliability:
        limitations.append("部分資訊僅有低可靠來源（如論壇匿名評論），建議求職者多方查證。")
    if gender_cat.summary == "資料不足":
        limitations.append("目前缺少公司官方性別平等或 DEI 政策來源。")
    if acc_cat.summary == "資料不足":
        limitations.append("目前缺少公司對於無障礙面試與工作環境的具體說明。")

    return CompanyInclusionAnalysis(
        company_name=company_name,
        overall_summary=overall,
        gender_inclusion=gender_cat,
        accessibility_support=acc_cat,
        workplace_safety_and_fairness=safety_cat,
        interview_questions_to_confirm=[
            "公司是否有正式反歧視與反騷擾政策？",
            "面試若需要手語翻譯、字幕或書面題目，是否可以提前安排？",
            "若需要無障礙面試場地或遠端面試，公司是否可協助？",
            "公司是否有正式申訴或員工協助管道？"
        ],
        evidence_limitations=limitations
    )
