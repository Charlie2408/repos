# Open-Meteo 天气数据接口自动化测试项目

基于 **Python + pytest + requests** 对 [Open-Meteo](https://open-meteo.com/) 免费天气 API 的 `/v1/forecast`
接口开展接口自动化测试。无需 API Key，可在公网直接访问，适合作为软件测试实习简历中的实战项目。

## 一、项目结构

```
open-meteo-api-test/
├── config.py                     # API 地址、超时、合法天气码等全局配置
├── requirements.txt              # 依赖清单
├── run_all.bat                   # 一键安装依赖并运行测试、生成报告
├── README.md
├── utils/
│   ├── api_client.py             # requests 会话封装（APIClient）
│   └── data_validator.py         # 响应字段完整性 / 取值范围 / 经纬度校验
├── test_api/
│   ├── conftest.py               # pytest 全局夹具（客户端、默认参数）
│   ├── test_forecast_function.py # 功能测试：正常参数（TC-001/002/005）
│   ├── test_forecast_boundary.py # 边界值测试：经纬度边界（TC-003/004）
│   ├── test_forecast_param.py    # 异常参数：非法/缺失/类型错误（TC-006~009）
│   ├── test_forecast_data_driven.py  # 数据驱动：多城市坐标（TC-010）
│   └── test_forecast_response.py # 响应数据合法性校验（TC-011/012）
├── testcases/
│   └── Open-Meteo接口测试用例.xlsx  # 接口测试用例设计表（12 条用例）
└── reports/
    └── report.html               # pytest-html 测试报告
```

## 二、测试范围

- **功能测试**：指定天气变量与时区、简化参数 `current_weather=true`、中心经纬度等正常场景
- **边界值测试**：纬度 ±90°、经度 ±180° 上下边界
- **异常参数测试**：纬度/经度越界、缺失必填参数、参数类型错误（返回 400 及错误提示）
- **数据驱动测试**：北京/上海/纽约/伦敦/东京等多城市坐标参数化批量执行
- **响应数据校验**：`current_weather` 字段完整性、温度/风速/风向/昼夜/天气码取值区间合法性

## 三、运行方式

```bash
# 方式一：一键运行（自动安装依赖 + 执行测试 + 生成 HTML 报告）
run_all.bat

# 方式二：手动执行
pip install -r requirements.txt
python -m pytest test_api -v --html=reports/report.html --self-contained-html
```

测试报告生成在 `reports/report.html`，可用浏览器打开查看。

## 四、测试用例设计方法

- **等价类划分**：正常参数、边界参数、非法参数分类设计用例
- **边界值分析**：经纬度取值边界重点覆盖
- **数据驱动**：多城市坐标参数化，提高用例复用性与覆盖率
- **断言设计**：状态码、响应结构、字段取值范围、错误信息多维度校验
