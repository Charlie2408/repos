# -*- coding: utf-8 -*-
"""API 客户端：封装 requests 会话，统一处理请求与响应"""
import requests
import config


class APIClient:
    """Open-Meteo 接口客户端"""

    def __init__(self, base_url=config.BASE_URL, timeout=config.TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def get_forecast(self, params):
        """GET /v1/forecast，返回原始 response 对象"""
        return self.session.get(self.base_url, params=params, timeout=self.timeout)
