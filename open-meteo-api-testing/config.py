# -*- coding: utf-8 -*-
"""Open-Meteo 天气 API 接口测试工程 - 全局配置"""

# API 基础地址
BASE_URL = "https://api.open-meteo.com/v1/forecast"

# 请求超时（秒）
TIMEOUT = 30

# 合法 WMO 天气代码集合（用于响应数据合法性校验）
VALID_WEATHER_CODES = {
    0, 1, 2, 3, 45, 48, 51, 53, 55, 56, 57,
    61, 63, 65, 66, 67, 71, 73, 75, 77,
    80, 81, 82, 85, 86, 95, 96, 99,
}
