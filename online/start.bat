@echo off
chcp 65001 >nul
echo ==================================
echo 简历信息提取系统 - 线上部署版
echo ==================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到 Python，请先安装 Python
    pause
    exit /b 1
)

REM 检查依赖是否安装
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  检测到未安装依赖，正在安装...
    pip install -r requirements-compatible.txt
    echo.
)

REM 创建必要的目录
if not exist uploads mkdir uploads

echo ✅ 准备就绪，正在启动服务...
echo.

REM 启动应用
python app.py

pause

