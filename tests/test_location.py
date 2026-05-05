from app.normalizers.location import normalize_location

def test_location_normalization():
    # 台北市信義區
    assert normalize_location("台北市信義區") == "台北市"
    
    # 台北信義區
    assert normalize_location("台北信義區") == "台北市"
    
    # 新北市板橋區
    assert normalize_location("新北市板橋區") == "新北市"
    
    # 遠端工作
    assert normalize_location("遠端工作") == "遠端"
    
    # 空字串
    assert normalize_location("") == "未知"
    assert normalize_location(None) == "未知"
