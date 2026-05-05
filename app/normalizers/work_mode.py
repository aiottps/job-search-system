def normalize_work_mode(jd_text: str, location_text: str) -> str:
    """
    Determines work mode: onsite, remote, hybrid, or unknown.
    """
    combined = (jd_text or "") + " " + (location_text or "")
    combined = combined.lower()
    
    # Negative remote keywords (interviews, meetings, etc.)
    negative_remote_keywords = [
        "遠端面試", "線上面試", "視訊面試", "視訊面談", "線上對談",
        "online interview", "remote interview", "video interview", "video call interview"
    ]
    
    for kw in negative_remote_keywords:
        combined = combined.replace(kw, "")

    hybrid_keywords = ["混合", "hybrid", "部分遠端", "每週可遠端", "彈性遠端", "wfh", "彈性辦公"]
    onsite_keywords = ["需進辦公室", "現場辦公", "駐點", "不可遠端", "onsite", "進駐"]
    remote_keywords = ["全遠端", "完全遠端", "remote work", "fully remote", "100% remote"]
    
    # Priority: Hybrid > Remote > Onsite
    for kw in hybrid_keywords:
        if kw in combined:
            return "hybrid"
            
    for kw in remote_keywords:
        if kw in combined:
            return "remote"
            
    # Simple check for general remote if not already caught
    if "遠端" in combined or "remote" in combined:
        return "remote"

    for kw in onsite_keywords:
        if kw in combined:
            return "onsite"
        
    return "unknown"
