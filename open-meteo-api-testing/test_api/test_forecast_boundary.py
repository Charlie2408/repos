# -*- coding: utf-8 -*-
"""边界值测试：经纬度取值边界（对应 TC-003 / TC-004）"""
from utils.data_validator import check_coordinates


def test_tc003_upper_boundary_lat90_lon180(client):
    """TC-003 上边界 lat=90 / lon=180：返回经纬度应在合法范围内"""
    params = {"latitude": "90", "longitude": "180", "current_weather": "true"}
    resp = client.get_forecast(params)
    assert resp.status_code == 200, "状态码应为 200，实际 %s" % resp.status_code
    data = resp.json()
    ok, errors = check_coordinates(data)
    assert ok, "边界经纬度越界: %s" % errors
    assert "current_weather" in data, "缺少 current_weather 字段"


def test_tc004_lower_boundary_lat_minus90_lon_minus180(client):
    """TC-004 下边界 lat=-90 / lon=-180：返回经纬度应在合法范围内"""
    params = {"latitude": "-90", "longitude": "-180", "current_weather": "true"}
    resp = client.get_forecast(params)
    assert resp.status_code == 200, "状态码应为 200，实际 %s" % resp.status_code
    data = resp.json()
    ok, errors = check_coordinates(data)
    assert ok, "边界经纬度越界: %s" % errors
    assert "current_weather" in data, "缺少 current_weather 字段"
