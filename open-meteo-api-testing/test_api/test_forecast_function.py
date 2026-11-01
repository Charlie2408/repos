# -*- coding: utf-8 -*-
"""功能测试：正常参数下的接口行为（对应 TC-001 / TC-002 / TC-005）"""


def test_tc001_specific_current_variables_and_timezone(client):
    """TC-001 指定天气变量 + 指定时区，校验返回与请求一致"""
    params = {
        "latitude": "30.67",
        "longitude": "104.06",
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "Asia/Shanghai",
    }
    resp = client.get_forecast(params)
    assert resp.status_code == 200, "状态码应为 200，实际 %s" % resp.status_code
    data = resp.json()

    # 响应存在 current 与 current_units
    assert "current" in data, "缺少 current 字段"
    assert "current_units" in data, "缺少 current_units 字段"
    # 三个天气变量及其单位都存在
    for var in ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"]:
        assert var in data["current"], "current 缺少变量 %s" % var
        assert var in data["current_units"], "current_units 缺少单位 %s" % var
    # 返回时区与请求一致
    assert data.get("timezone") == "Asia/Shanghai", (
        "返回时区应为 Asia/Shanghai，实际 %s" % data.get("timezone"))


def test_tc002_simple_current_weather(client, valid_params):
    """TC-002 current_weather=true 简化参数，校验 current_weather 结构"""
    resp = client.get_forecast(valid_params)
    assert resp.status_code == 200, "状态码应为 200，实际 %s" % resp.status_code
    data = resp.json()
    assert "current_weather" in data, "缺少 current_weather 字段"
    assert "current_weather_units" in data, "缺少 current_weather_units 字段"
    for field in ["time", "interval", "temperature", "windspeed",
                  "winddirection", "is_day", "weathercode"]:
        assert field in data["current_weather"], "current_weather 缺少字段 %s" % field


def test_tc005_zero_coordinates(client):
    """TC-005 中心点经纬度 (0,0)，校验正常返回"""
    params = {"latitude": "0", "longitude": "0", "current_weather": "true"}
    resp = client.get_forecast(params)
    assert resp.status_code == 200, "状态码应为 200，实际 %s" % resp.status_code
    assert "current_weather" in resp.json(), "缺少 current_weather 字段"
