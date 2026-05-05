from app.normalizers.salary import parse_salary

def test_salary_parsing():
    # 月薪 50,000 - 80,000
    res = parse_salary("月薪 50,000 - 80,000")
    assert res.annual_min == 600000
    assert res.annual_max == 960000
    assert not res.is_estimated

    # 月薪 4.5萬 - 6萬
    res = parse_salary("月薪 4.5萬 - 6萬")
    assert res.annual_min == 540000
    assert res.annual_max == 720000
    assert not res.is_estimated

    # 年薪 70萬 - 100萬
    res = parse_salary("年薪 70萬 - 100萬")
    assert res.annual_min == 700000
    assert res.annual_max == 1000000
    assert not res.is_estimated

    # 年薪 1,000,000 - 1,500,000
    res = parse_salary("年薪 1,000,000 - 1,500,000")
    assert res.annual_min == 1000000
    assert res.annual_max == 1500000
    assert not res.is_estimated

    # 年薪 1.2百萬
    res = parse_salary("年薪 1.2百萬")
    assert res.annual_min == 1200000
    assert res.annual_max == 1200000

    # 面議（經常性薪資達4萬元或以上）
    res = parse_salary("面議（經常性薪資達4萬元或以上）")
    assert res.annual_min == 480000
    assert res.is_estimated
    assert "4 萬元以上" in res.note

    # 待遇依公司規定
    res = parse_salary("待遇依公司規定")
    assert res.annual_min is None
    assert "依公司規定" in res.note
