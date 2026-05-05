from app.normalizers.work_mode import normalize_work_mode

def test_work_mode_normalization():
    # 全遠端
    assert normalize_work_mode("JD 內容...", "全遠端") == "remote"
    
    # 每週可遠端 2 天
    assert normalize_work_mode("每週可遠端 2 天", "台北市") == "hybrid"
    
    # 遠端面試，需進辦公室
    assert normalize_work_mode("遠端面試，需進辦公室", "台北市") == "onsite"
    
    # 視訊面談，駐點客戶端
    assert normalize_work_mode("視訊面談，駐點客戶端", "台北市") == "onsite"
    
    # 彈性辦公
    assert normalize_work_mode("提供彈性辦公時間與地點", "台北市") == "hybrid"
    
    # 無相關描述
    assert normalize_work_mode("一般軟體開發...", "台北市") == "unknown"
