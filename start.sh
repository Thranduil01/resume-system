#!/bin/bash
echo "===================================================="
echo "📋 简历信息提取系统 - 启动脚本"
echo "===================================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python 3"
    echo "   请先安装 Python 3.7 或更高版本"
    exit 1
fi

echo "🔍 检查环境..."
python3 check_environment.py

if [ $? -eq 0 ]; then
    echo ""
    echo "===================================================="
    echo "✅ 环境检查通过，正在启动系统..."
    echo "===================================================="
    echo ""
    
    # 停止旧进程
    lsof -ti:5001 | xargs kill -9 2>/dev/null
    
    # 启动服务器
    python3 app.py
else
    echo ""
    echo "===================================================="
    echo "❌ 环境检查失败"
    echo "===================================================="
    echo ""
    echo "最小安装（仅文本型 PDF）："
    echo "  pip3 install -r requirements-minimal.txt"
    echo ""
    echo "推荐安装（支持扫描版 PDF）："
    echo "  pip3 install -r requirements-minimal.txt"
    echo "  pip3 install -r requirements-ocr.txt"
    echo "  brew install tesseract tesseract-lang poppler"
    echo ""
    exit 1
fi

