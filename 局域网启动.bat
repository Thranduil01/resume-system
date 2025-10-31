@echo off
chcp 65001 >nul
title 简历信息提取系统 - 局域网部署版

echo ====================================
echo 🌐 启动简历信息提取系统（局域网版）
echo ====================================
echo.

REM 切换到脚本所在目录
cd /d "%~dp0"

REM 检查 Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 错误：未找到 Python
    echo 请先安装 Python: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查依赖
python -c "import flask" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 📦 首次运行，正在安装依赖...
    echo    （自动选择兼容版本，可能需要1-2分钟）
    echo.
    
    REM 优先尝试兼容版本
    if exist requirements-compatible.txt (
        pip install -r requirements-compatible.txt
    ) else (
        pip install -r requirements-minimal.txt
    )
    
    echo.
)

REM 获取本机局域网 IP
echo 🔍 正在获取局域网 IP...
echo.

REM Windows 获取 IP
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    set LOCAL_IP=%%a
    goto :found_ip
)

:found_ip
REM 去除空格
set LOCAL_IP=%LOCAL_IP: =%

if "%LOCAL_IP%"=="" (
    echo ⚠️  警告：无法自动获取局域网 IP
    echo    请手动查看 IP 地址：
    echo    控制面板 → 网络和 Internet → 网络连接
    set LOCAL_IP=your-ip-address
)

REM 显示访问信息
echo ====================================
echo ✅ 系统启动中...
echo ====================================
echo.
echo 📍 本机访问地址：
echo    http://localhost:5001
echo.
echo 🌐 局域网访问地址（分享给同事）：
echo    http://%LOCAL_IP%:5001
echo.
echo 📋 使用说明：
echo    1. 你的电脑必须一直开着
echo    2. 同事需要连接同一个 WiFi
echo    3. 把局域网地址发给同事即可
echo.
echo ⚠️  注意：
echo    - 关闭此窗口会停止服务
echo    - 按 Ctrl+C 可以停止服务
echo.
echo ====================================
echo.

REM 启动服务
python app.py

REM 保持窗口打开
pause



