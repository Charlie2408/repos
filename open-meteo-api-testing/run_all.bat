@echo off
chcp 65001 >nul
echo ============================================
echo  Open-Meteo API 接口自动化测试
echo ============================================
cd /d "%~dp0"

echo [1/3] 检查并安装依赖...
python -m pip install -r requirements.txt -q

echo [2/3] 运行 pytest 并生成 HTML 报告...
python -m pytest test_api -v --html=reports/report.html --self-contained-html
if %errorlevel% neq 0 (
    echo 测试执行出错，请检查上方日志
    pause
    exit /b 1
)

echo [3/3] 完成，报告已生成: reports\report.html
pause