# -*- coding: utf-8 -*-
"""响应数据合法性校验（对应 TC-011 / TC-012）"""
from utils.data_validator import (
    check_current_weather_fields, check_field_ranges,
)


def test_tc011_current_weather_field_completeness(client, valid_params):
    """TC-011 current_weather 七个必填字段完整性"""
    resp = client.get_forecast(valid_params)
    assert resp.status_code == 200, "状态码应为 200，实际 %s" % resp.status_code
    cw = resp.json()["current_weather"]
    ok, missing = check_current_weather_fields(cw)
    assert ok, "current_weather 缺失字段: %s" % missing


def test_tc012_field_value_ranges(client, valid_params):
    """TC-012 温度/风速/风向/昼夜/天气码取值区间合法性"""
    resp = client.get_forecast(valid_params)
    assert resp.status_code == 200, "状态码应为 200，实际 %s" % resp.status_code
    cw = resp.json()["current_weather"]
    ok, errors = check_field_ranges(cw)
    assert ok, "字段取值非法: %s" % errors
