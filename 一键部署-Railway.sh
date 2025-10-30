#!/bin/bash

# 🚀 Railway 一键部署脚本
# 跳过 GitHub，直接部署到 Railway

echo "🎯 Railway 一键部署脚本"
echo "===================================="
echo ""

# 检查是否已安装 npm
if ! command -v npm &> /dev/null; then
    echo "❌ 错误：未安装 npm"
    echo "请先安装 Node.js: https://nodejs.org/"
    exit 1
fi

echo "✅ npm 已安装"
echo ""

# 检查是否已安装 Railway CLI
if ! command -v railway &> /dev/null; then
    echo "📦 正在安装 Railway CLI..."
    npm install -g @railway/cli
    
    if [ $? -ne 0 ]; then
        echo "❌ Railway CLI 安装失败"
        echo "请手动运行: npm install -g @railway/cli"
        exit 1
    fi
    
    echo "✅ Railway CLI 安装成功"
else
    echo "✅ Railway CLI 已安装"
fi

echo ""
echo "🔐 正在登录 Railway..."
echo "（浏览器会自动打开，请在浏览器中授权）"
echo ""

railway login

if [ $? -ne 0 ]; then
    echo "❌ 登录失败"
    exit 1
fi

echo ""
echo "✅ 登录成功"
echo ""

# 检查是否已初始化项目
if [ ! -f ".railway/config.json" ]; then
    echo "🎬 正在初始化 Railway 项目..."
    railway init
    
    if [ $? -ne 0 ]; then
        echo "❌ 初始化失败"
        exit 1
    fi
    
    echo "✅ 项目初始化成功"
else
    echo "✅ 项目已初始化"
fi

echo ""
echo "🚀 正在部署..."
echo "（可能需要 3-5 分钟，请耐心等待）"
echo ""

railway up

if [ $? -ne 0 ]; then
    echo "❌ 部署失败"
    echo "请检查错误信息或手动运行: railway up"
    exit 1
fi

echo ""
echo "✅ 部署成功！"
echo ""

echo "🌐 正在生成访问域名..."
railway domain

echo ""
echo "===================================="
echo "🎉 部署完成！"
echo ""
echo "📋 后续操作："
echo "  1. 访问 Railway 仪表板: railway open"
echo "  2. 查看实时日志: railway logs"
echo "  3. 查看域名: railway domain"
echo ""
echo "💡 提示："
echo "  - 域名可能需要几分钟才能生效"
echo "  - 首次启动可能较慢（安装依赖）"
echo "  - 使用 '☁️ 文件上传' 模式上传 PDF"
echo ""
echo "===================================="

