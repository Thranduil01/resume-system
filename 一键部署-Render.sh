#!/bin/bash

# 🚀 Render 部署准备脚本
# 帮助你快速准备推送到 GitHub，然后在 Render 部署

echo "🎯 Render 部署准备脚本"
echo "===================================="
echo ""

# 检查是否在正确的目录
if [ ! -f "app.py" ]; then
    echo "❌ 错误：请在项目根目录运行此脚本"
    exit 1
fi

echo "✅ 项目目录正确"
echo ""

# 检查 Git 状态
echo "🔍 检查 Git 状态..."
if [ ! -d ".git" ]; then
    echo "❌ 错误：Git 仓库未初始化"
    exit 1
fi

echo "✅ Git 仓库已初始化"
echo ""

# 检查是否有未提交的更改
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  检测到未提交的更改"
    echo "📝 正在提交更改..."
    git add .
    git commit -m "Update: Prepare for Render deployment"
    echo "✅ 更改已提交"
else
    echo "✅ 没有未提交的更改"
fi

echo ""
echo "===================================="
echo "📋 下一步操作指南"
echo "===================================="
echo ""

echo "步骤1：创建新的 GitHub 仓库（如果旧的有问题）"
echo "  1. 访问：https://github.com/new"
echo "  2. 仓库名：resume-system"
echo "  3. ⚠️  不要勾选任何初始化选项"
echo "  4. 点击 'Create repository'"
echo ""

echo "步骤2：推送代码到 GitHub"
echo "  方式1（HTTPS - 需要 Token）："
echo "    git remote set-url origin https://github.com/Thranduil01/resume-system.git"
echo "    git push -u origin main"
echo ""
echo "  方式2（SSH - 如果已配置）："
echo "    git remote set-url origin git@github.com:Thranduil01/resume-system.git"
echo "    git push -u origin main"
echo ""

echo "步骤3：在 Render 部署"
echo "  1. 访问：https://render.com"
echo "  2. 使用 GitHub 账号登录"
echo "  3. 点击 'New +' → 'Web Service'"
echo "  4. 连接你的 GitHub 仓库"
echo "  5. 选择 'resume-system' 仓库"
echo "  6. 配置："
echo "     Name: resume-system"
echo "     Runtime: Python 3"
echo "     Build Command: pip install -r requirements-minimal.txt"
echo "     Start Command: python app.py"
echo "  7. 选择 'Free' 计划"
echo "  8. 点击 'Create Web Service'"
echo ""

echo "===================================="
echo "💡 提示"
echo "===================================="
echo ""
echo "1. Render 完全免费，不需要信用卡"
echo "2. 部署需要 3-5 分钟"
echo "3. 应用 15 分钟无活动会休眠（正常现象）"
echo "4. 下次访问会自动唤醒（约 30 秒）"
echo "5. 使用 '☁️ 文件上传' 模式上传 PDF"
echo ""

echo "===================================="
echo "📚 详细文档"
echo "===================================="
echo ""
echo "查看 'Render部署指南.md' 了解详细步骤"
echo ""

# 询问是否需要帮助推送
echo "是否要现在推送到 GitHub？(y/n)"
read -r response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo ""
    echo "请选择推送方式："
    echo "1. HTTPS（需要 GitHub Token）"
    echo "2. SSH（需要已配置 SSH Key）"
    read -r method
    
    if [ "$method" = "1" ]; then
        echo ""
        echo "🔧 设置 HTTPS 远程地址..."
        git remote set-url origin https://github.com/Thranduil01/resume-system.git
        echo "✅ 远程地址已设置"
        echo ""
        echo "🚀 推送到 GitHub..."
        echo "（需要输入 GitHub 用户名和 Token）"
        git push -u origin main
    elif [ "$method" = "2" ]; then
        echo ""
        echo "🔧 设置 SSH 远程地址..."
        git remote set-url origin git@github.com:Thranduil01/resume-system.git
        echo "✅ 远程地址已设置"
        echo ""
        echo "🚀 推送到 GitHub..."
        git push -u origin main
    else
        echo "❌ 无效选项"
        exit 1
    fi
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ 推送成功！"
        echo ""
        echo "🎉 下一步："
        echo "   访问 https://render.com 完成部署"
    else
        echo ""
        echo "❌ 推送失败"
        echo "   请查看错误信息并手动推送"
    fi
else
    echo ""
    echo "📋 记得手动推送代码到 GitHub，然后在 Render 部署"
fi

echo ""
echo "===================================="

