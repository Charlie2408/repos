# -*- coding: utf-8 -*-
"""异常参数测试：非法值、缺失必填、类型错误（对应 TC-006 ~ TC-009）"""


def test_tc006_latitude_out_of_range(client):
    """TC-006 纬度超上界 lat=91 → 应返回 400 及 error 提示"""
    params = {"latitude": "91", "longitude": "13.41", "current_weather": "true"}
    resp = client.get_forecast(params)
    assert resp.status_code == 400, "状态码应为 400，实际 %s" % resp.status_code
    body = resp.json()
    assert body.get("error") is True, "应返回 error=true"
    assert "Latitude must be in range of -90 to 90" in body.get("reason", ""), (
        "错误信息应提示纬度范围，实际: %s" % body.get("reason"))


def test_tc007_longitude_out_of_range(client):
    """TC-007 经度超上界 lon=181 → 应返回 400 及 error 提示"""
    params = {"latitude": "30", "longitude": "181", "current_weather": "true"}
    resp = client.get_forecast(params)
    assert resp.status_code == 400, "状态码应为 400，实际 %s" % resp.status_code
    body = resp.json()
    assert body.get("error") is True, "应返回 error=true"
    assert "Longitude must be in range of -180 to 180" in body.get("reason", ""), (
        "错误信息应提示经度范围，实际: %s" % body.get("reason"))


def test_tc008_missing_latitude(client):
    """TC-008 缺失必填参数 latitude → 应返回 400"""
    params = {"longitude": "13.41", "current_weather": "true"}
    resp = client.get_forecast(params)
    assert resp.status_code == 400, "状态码应为 400，实际 %s" % resp.status_code
    body = resp.json()
    assert body.get("error") is True, "应返回 error=true"


def test_tc009_latitude_non_numeric(client):
    """TC-009 类型错误 lat=abc → 应返回 400 及解析失败提示"""
    params = {"latitude": "abc", "longitude": "13.41", "current_weather": "true"}
    resp = client.get_forecast(params)
    assert resp.status_code == 400, "状态码应为 400，实际 %s" % resp.status_code
    body = resp.json()
    assert body.get("error") is True, "应返回 error=true"
    assert "Cannot initialize Float" in body.get("reason", ""), (
        "错误信息应提示无法解析为数值，实际: %s" % body.get("reason"))
