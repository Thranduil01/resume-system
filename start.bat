@echo off
REM 简历信息提取系统 - Windows 启动脚本

echo ==================================
echo 启动简历信息提取系统
echo ==================================
echo.

REM 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未找到 Python
    echo 请先安装 Python: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查依赖
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo 首次运行，正在安装依赖...
    pip install -r requirements-minimal.txt
    echo.
)

REM 启动服务
echo 正在启动服务器...
echo.
python app.py

pause

