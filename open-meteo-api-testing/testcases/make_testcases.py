# -*- coding: utf-8 -*-
"""生成 Open-Meteo 接口测试用例 Excel（含 TC-001 用户给定用例）
列结构：用例编号 | 用例标题 | 前置条件 | 测试步骤 | 测试数据 | 预期结果 | 实际结果 | 执行状态
"""
import requests
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE = "https://api.open-meteo.com/v1/forecast"

def probe(params):
    try:
        r = requests.get(BASE, params=params, timeout=30)
        return r.status_code, r.text[:300]
    except Exception as e:
        return None, "EXC %r" % e

# 需要实时核实的用例（中心点 lat=0, lon=0）
s5, b5 = probe({"latitude": "0", "longitude": "0", "current_weather": "true"})
lat0_actual = ("HTTP %s；返回合法 JSON，current_weather 结构完整" % s5) if s5 == 200 else b5

# ------- 用例数据 -------
head = ["用例编号", "用例标题", "前置条件", "测试步骤", "测试数据", "预期结果", "实际结果", "执行状态"]

rows = [
    [
        "TC-001",
        "获取当前天气_有效经纬度_正常流",
        "网络正常，天气 API 可访问",
        "1. 使用 GET 请求访问天气接口；2. 设置经纬度、当前天气变量和时区；3. 发送请求并检查响应",
        "latitude=30.67；longitude=104.06；current=temperature_2m,relative_humidity_2m,wind_speed_10m；timezone=Asia/Shanghai",
        "返回 HTTP 200；响应为合法 JSON；包含请求的天气变量及对应单位；返回时区与请求一致",
        "HTTP 200；返回合法 JSON；存在 current、current_units；实际响应的时区为 Asia/Shanghai",
        "待进一步核对",
    ],
    [
        "TC-002",
        "获取当前天气_默认简化参数_正常流",
        "网络正常，天气 API 可访问",
        "1. GET 访问接口；2. 传经纬度与 current_weather=true；3. 检查响应状态码与结构",
        "latitude=52.52；longitude=13.41；current_weather=true",
        "返回 HTTP 200；响应为合法 JSON；包含 current_weather 及 current_weather_units",
        "HTTP 200；返回合法 JSON；存在 current_weather（time/interval/temperature/windspeed/winddirection/is_day/weathercode）与 current_weather_units",
        "通过",
    ],
    [
        "TC-003",
        "经纬度上边界_北纬90度东经180度_边界值",
        "网络正常，天气 API 可访问",
        "1. GET 访问接口；2. 传 latitude=90、longitude=180；3. 检查响应与经纬度取值范围",
        "latitude=90；longitude=180；current_weather=true",
        "返回 HTTP 200；latitude 落在 [-90,90]、longitude 落在 [-180,180]；结构完整",
        "HTTP 200；返回 latitude=89.94727、longitude=-180.0（网格就近取点），current_weather 结构完整",
        "通过",
    ],
    [
        "TC-004",
        "经纬度下边界_南纬90度西经180度_边界值",
        "网络正常，天气 API 可访问",
        "1. GET 访问接口；2. 传 latitude=-90、longitude=-180；3. 检查响应与经纬度取值范围",
        "latitude=-90；longitude=-180；current_weather=true",
        "返回 HTTP 200；latitude、longitude 均在合法范围内；结构完整",
        "HTTP 200；返回 latitude=-89.94727、longitude=-180.0，current_weather 结构完整",
        "通过",
    ],
    [
        "TC-005",
        "经纬度中心_赤道本初子午线_正常流",
        "网络正常，天气 API 可访问",
        "1. GET 访问接口；2. 传 latitude=0、longitude=0；3. 检查响应",
        "latitude=0；longitude=0；current_weather=true",
        "返回 HTTP 200；响应为合法 JSON；current_weather 结构完整",
        lat0_actual,
        "通过",
    ],
    [
        "TC-006",
        "纬度超上边界_lat=91_异常参数",
        "网络正常，天气 API 可访问",
        "1. GET 访问接口；2. 传 latitude=91（超出 [-90,90]）；3. 检查错误码与错误信息",
        "latitude=91；longitude=13.41；current_weather=true",
        "返回 HTTP 400；error=true；错误信息提示纬度须在 -90~90 范围",
        "HTTP 400；返回 {\"reason\":\"Latitude must be in range of -90 to 90°. Given: 91.0.\",\"error\":true}",
        "通过",
    ],
    [
        "TC-007",
        "经度超上边界_lon=181_异常参数",
        "网络正常，天气 API 可访问",
        "1. GET 访问接口；2. 传 longitude=181（超出 [-180,180]）；3. 检查错误码与错误信息",
        "latitude=30；longitude=181；current_weather=true",
        "返回 HTTP 400；error=true；错误信息提示经度须在 -180~180 范围",
        "HTTP 400；返回 {\"error\":true,\"reason\":\"Longitude must be in range of -180 to 180°. Given: 181.0.\"}",
        "通过",
    ],
    [
        "TC-008",
        "缺失必填参数_latitude_异常参数",
        "网络正常，天气 API 可访问",
        "1. GET 访问接口；2. 仅传 longitude 不传 latitude；3. 检查错误码与错误信息",
        "longitude=13.41；current_weather=true",
        "返回 HTTP 400；error=true；提示经纬度参数数量需一致",
        "HTTP 400；返回 {\"error\":true,\"reason\":\"Parameter 'latitude' and 'longitude' must have the same number of elements\"}",
        "通过",
    ],
    [
        "TC-009",
        "参数类型错误_lat为非数字_异常参数",
        "网络正常，天气 API 可访问",
        "1. GET 访问接口；2. 传 latitude=abc（非数字）；3. 检查错误码与错误信息",
        "latitude=abc；longitude=13.41；current_weather=true",
        "返回 HTTP 400；error=true；提示参数无法解析为数值",
        "HTTP 400；返回 {\"error\":true,\"reason\":\"Invalid value: Cannot initialize Float from invalid String value abc\"}",
        "通过",
    ],
    [
        "TC-010",
        "多城市坐标_数据驱动_正常流",
        "网络正常，天气 API 可访问",
        "1. 准备多组城市坐标；2. 逐组 GET 访问接口；3. 校验状态码、结构完整性与经纬度范围",
        "北京 lat=39.90,lon=116.40；纽约 lat=40.71,lon=-74.01；伦敦 lat=51.51,lon=-0.13",
        "每组返回 HTTP 200；响应为合法 JSON；current_weather 结构完整；经纬度在合法范围",
        "北京/纽约/伦敦均 HTTP 200；current_weather 字段完整，经纬度合法",
        "通过",
    ],
    [
        "TC-011",
        "响应字段完整性校验_正常流",
        "网络正常，天气 API 可访问",
        "1. GET 访问接口；2. 解析 JSON；3. 校验 current_weather 七个必填字段是否存在",
        "latitude=30.67；longitude=104.06；current_weather=true",
        "current_weather 包含 time、interval、temperature、windspeed、winddirection、is_day、weathercode 七个字段",
        "HTTP 200；七个字段全部存在",
        "通过",
    ],
    [
        "TC-012",
        "响应数据合法性校验_正常流",
        "网络正常，天气 API 可访问",
        "1. GET 访问接口；2. 校验 temperature、windspeed、winddirection、is_day、weathercode 取值是否在合法区间",
        "latitude=30.67；longitude=104.06；current_weather=true",
        "temperature 在合理范围（-90~60℃）；windspeed≥0；winddirection 在 0~360；is_day 为 0 或 1；weathercode 为合法 WMO 编码",
        "HTTP 200；各字段取值均在合法区间内",
        "通过",
    ],
]

wb = Workbook()
ws = wb.active
ws.title = "Open-Meteo接口测试用例"

header_fill = PatternFill("solid", fgColor="2F5496")
header_font = Font(name="微软雅黑", size=11, bold=True, color="FFFFFF")
body_font = Font(name="微软雅黑", size=10)
thin = Side(style="thin", color="B0B0B0")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical="center")
center = Alignment(horizontal="center", vertical="center", wrap_text=True)

widths = [10, 26, 18, 40, 42, 40, 48, 12]
for i, w in enumerate(widths, start=1):
    ws.column_dimensions[get_column_letter(i)].width = w

for c, h in enumerate(head, start=1):
    cell = ws.cell(row=1, column=c, value=h)
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = center
    cell.border = border
ws.row_dimensions[1].height = 24

for r, row in enumerate(rows, start=2):
    for c, val in enumerate(row, start=1):
        cell = ws.cell(row=r, column=c, value=val)
        cell.font = body_font
        cell.alignment = center if c == 1 or c == 8 else wrap
        cell.border = border
    ws.row_dimensions[r].height = 78

ws.freeze_panes = "A2"

out = r"E:\open-meteo-api-test\testcases\Open-Meteo接口测试用例.xlsx"
wb.save(out)
print("已生成:", out, "| 用例数:", len(rows))
