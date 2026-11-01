# -*- coding: utf-8 -*-
"""响应数据校验工具：字段完整性、取值范围、结构合法性"""
import config

# current_weather 七个必填字段
CURRENT_WEATHER_FIELDS = [
    "time", "interval", "temperature",
    "windspeed", "winddirection", "is_day", "weathercode",
]

# 温度合理区间（℃）：地球极端气温大致 -90 ~ 60
TEMP_MIN, TEMP_MAX = -90.0, 60.0


def check_current_weather_fields(current_weather):
    """校验 current_weather 是否包含全部七个字段，返回 (ok, 缺失字段列表)"""
    missing = [f for f in CURRENT_WEATHER_FIELDS if f not in current_weather]
    return (len(missing) == 0), missing


def check_field_ranges(cw):
    """校验各字段取值是否在合法区间，返回 (ok, 异常项列表)"""
    errors = []

    temp = cw.get("temperature")
    if temp is not None and not (TEMP_MIN <= temp <= TEMP_MAX):
        errors.append("temperature=%.1f 超出合法区间 [%s, %s]" % (temp, TEMP_MIN, TEMP_MAX))

    wind = cw.get("windspeed")
    if wind is not None and wind < 0:
        errors.append("windspeed=%.1f 不能为负" % wind)

    direction = cw.get("winddirection")
    if direction is not None and not (0 <= direction <= 360):
        errors.append("winddirection=%.1f 超出 [0,360]" % direction)

    is_day = cw.get("is_day")
    if is_day is not None and is_day not in (0, 1):
        errors.append("is_day=%s 必须为 0 或 1" % is_day)

    code = cw.get("weathercode")
    if code is not None and code not in config.VALID_WEATHER_CODES:
        errors.append("weathercode=%s 不是合法 WMO 编码" % code)

    return (len(errors) == 0), errors


def check_coordinates(data):
    """校验返回经纬度是否在合法范围，返回 (ok, 异常项列表)"""
    errors = []
    lat = data.get("latitude")
    lon = data.get("longitude")
    if lat is not None and not (-90 <= lat <= 90):
        errors.append("latitude=%s 超出 [-90,90]" % lat)
    if lon is not None and not (-180 <= lon <= 180):
        errors.append("longitude=%s 超出 [-180,180]" % lon)
    return (len(errors) == 0), errors
