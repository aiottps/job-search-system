TAIWAN_CITIES = [
    "台北市", "新北市", "桃園市", "台中市", "台南市", "高雄市",
    "基隆市", "新竹市", "嘉義市",
    "新竹縣", "苗栗縣", "彰化縣", "南投縣", "雲林縣", "嘉義縣",
    "屏東縣", "宜蘭縣", "花蓮縣", "台東縣",
    "澎湖縣", "金門縣", "連江縣"
]

def normalize_location(location_text: str) -> str:
    """
    Normalizes location to Traditional Chinese city names or '遠端'.
    """
    if not location_text:
        return "未知"
    
    location_text = location_text.strip()
    
    # Remote check
    if "遠端" in location_text or "Remote" in location_text.lower():
        return "遠端"
    
    for city in TAIWAN_CITIES:
        if city in location_text:
            return city
        # Handle cases like "台北" instead of "台北市"
        if city[:-1] in location_text:
            return city
            
    return location_text
