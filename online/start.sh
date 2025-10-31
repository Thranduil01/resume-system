#!/bin/bash

# 简历信息提取系统 - 线上版启动脚本

echo "=================================="
echo "简历信息提取系统 - 线上部署版"
echo "=================================="
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 Python3，请先安装 Python"
    exit 1
fi

# 检查依赖是否安装
if ! python3 -c "import flask" 2> /dev/null; then
    echo "⚠️  检测到未安装依赖，正在安装..."
    pip3 install -r requirements-compatible.txt
    echo ""
fi

# 创建必要的目录
mkdir -p uploads

echo "✅ 准备就绪，正在启动服务..."
echo ""

# 启动应用
python3 app.py

