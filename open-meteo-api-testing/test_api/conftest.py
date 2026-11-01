# -*- coding: utf-8 -*-
"""pytest 公共配置与夹具"""
import os
import sys

# 保证从任意目录运行 pytest 时都能导入项目根目录下的 config 与 utils
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pytest
from utils.api_client import APIClient


@pytest.fixture(scope="session")
def client():
    """全局复用同一 API 客户端会话"""
    return APIClient()


@pytest.fixture
def valid_params():
    """一条有效的默认请求参数（成都坐标）"""
    return {
        "latitude": "30.67",
        "longitude": "104.06",
        "current_weather": "true",
    }
