#!/bin/bash

# 简历信息提取系统 - 局域网部署版本
# 适用于公司/学校内部多人使用

# 切换到脚本所在目录
cd "$(dirname "$0")"

echo "===================================="
echo "🌐 启动简历信息提取系统（局域网版）"
echo "===================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 Python"
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

# 获取本机局域网 IP
echo "🔍 正在获取局域网 IP..."
echo ""

# macOS 获取 IP
LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)

if [ -z "$LOCAL_IP" ]; then
    echo "⚠️  警告：无法自动获取局域网 IP"
    echo "   请手动查看 IP 地址："
    echo "   系统偏好设置 → 网络 → 高级 → TCP/IP"
    LOCAL_IP="your-ip-address"
fi

# 显示访问信息
echo "===================================="
echo "✅ 系统启动中..."
echo "===================================="
echo ""
echo "📍 本机访问地址："
echo "   http://localhost:5001"
echo ""
echo "🌐 局域网访问地址（分享给同事）："
echo "   http://$LOCAL_IP:5001"
echo ""
echo "📋 使用说明："
echo "   1. 你的电脑必须一直开着"
echo "   2. 同事需要连接同一个 WiFi"
echo "   3. 把局域网地址发给同事即可"
echo ""
echo "⚠️  注意："
echo "   - 关闭此窗口会停止服务"
echo "   - 按 Ctrl+C 可以停止服务"
echo ""
echo "===================================="
echo ""

# 启动服务
python3 app.py

# 保持窗口打开
read -p "按回车键关闭..."



