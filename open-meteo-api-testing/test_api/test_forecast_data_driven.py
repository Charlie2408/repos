# -*- coding: utf-8 -*-
"""数据驱动测试：多城市坐标参数化（对应 TC-010）"""
import pytest
from utils.data_validator import check_coordinates

# 多城市坐标数据：城市名 -> (纬度, 经度)
CITIES = [
    ("北京", "39.90", "116.40"),
    ("上海", "31.23", "121.47"),
    ("纽约", "40.71", "-74.01"),
    ("伦敦", "51.51", "-0.13"),
    ("东京", "35.68", "139.69"),
]


@pytest.mark.parametrize("city,lat,lon", CITIES,
                         ids=[c[0] for c in CITIES])
def test_tc010_multiple_cities(client, city, lat, lon):
    """数据驱动：每组城市坐标应返回 200、结构完整、经纬度合法"""
    params = {"latitude": lat, "longitude": lon, "current_weather": "true"}
    resp = client.get_forecast(params)
    assert resp.status_code == 200, "[%s] 状态码应为 200，实际 %s" % (city, resp.status_code)
    data = resp.json()
    assert "current_weather" in data, "[%s] 缺少 current_weather 字段" % city
    ok, errors = check_coordinates(data)
    assert ok, "[%s] 经纬度越界: %s" % (city, errors)
