#!/bin/bash

# 简历信息提取系统 - 一键启动脚本
# 双击此文件即可启动

# 获取脚本所在目录
cd "$(dirname "$0")"

echo "=================================="
echo "🚀 启动简历信息提取系统"
echo "=================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python 3"
    echo "请先安装 Python: https://www.python.org/downloads/"
    read -p "按回车键退出..."
    exit 1
fi

# 检查依赖
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 首次运行，正在安装依赖..."
    echo "   （自动选择兼容版本，可能需要1-2分钟）"
    echo ""
    
    # 优先尝试兼容版本（不限制版本号）
    if [ -f "requirements-compatible.txt" ]; then
        pip3 install -r requirements-compatible.txt
    else
        pip3 install -r requirements-minimal.txt
    fi
    
    echo ""
fi

# 启动服务
echo "✅ 正在启动服务器..."
echo ""
python3 app.py

# 保持窗口打开
read -p "按回车键关闭..."

