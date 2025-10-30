#!/bin/bash

# 简历信息提取系统 - 快速部署脚本
# 适用于 Ubuntu/Debian 系统

echo "=================================="
echo "简历信息提取系统 - 快速部署"
echo "=================================="
echo ""

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then 
    echo "❌ 请使用 root 权限运行此脚本"
    echo "   sudo bash 快速部署.sh"
    exit 1
fi

# 1. 更新系统
echo "📦 更新系统..."
apt update && apt upgrade -y

# 2. 安装 Python3
echo "🐍 安装 Python3..."
apt install python3 python3-pip -y

# 3. 安装 OCR 环境（可选）
read -p "是否安装 OCR 环境？(y/n): " install_ocr
if [ "$install_ocr" = "y" ]; then
    echo "📷 安装 Tesseract OCR..."
    apt install tesseract-ocr tesseract-ocr-chi-sim poppler-utils -y
fi

# 4. 安装 Python 依赖
echo "📚 安装 Python 依赖..."
pip3 install -r requirements-minimal.txt

if [ "$install_ocr" = "y" ]; then
    pip3 install -r requirements-ocr.txt
fi

# 5. 安装生产服务器
echo "🚀 安装 Gunicorn..."
pip3 install gunicorn

# 6. 配置防火墙
echo "🔥 配置防火墙..."
ufw allow 5001
ufw --force enable

# 7. 是否配置为系统服务
read -p "是否配置为系统服务（开机自启）？(y/n): " setup_service
if [ "$setup_service" = "y" ]; then
    echo "⚙️  配置系统服务..."
    
    # 创建服务文件
    cat > /etc/systemd/system/resume-system.service << EOF
[Unit]
Description=Resume Information Extraction System
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    # 启用并启动服务
    systemctl daemon-reload
    systemctl enable resume-system
    systemctl start resume-system
    
    echo "✅ 系统服务已配置并启动"
    echo "   查看状态: systemctl status resume-system"
    echo "   查看日志: journalctl -u resume-system -f"
else
    # 直接启动
    echo "🚀 启动服务..."
    nohup python3 app.py > server.log 2>&1 &
    echo "✅ 服务已在后台启动"
fi

# 8. 显示访问信息
echo ""
echo "=================================="
echo "✅ 部署完成！"
echo "=================================="
echo ""
echo "访问地址："
echo "  http://$(hostname -I | awk '{print $1}'):5001"
echo ""
echo "常用命令："
if [ "$setup_service" = "y" ]; then
    echo "  启动服务: systemctl start resume-system"
    echo "  停止服务: systemctl stop resume-system"
    echo "  重启服务: systemctl restart resume-system"
    echo "  查看状态: systemctl status resume-system"
    echo "  查看日志: journalctl -u resume-system -f"
else
    echo "  查看日志: tail -f server.log"
    echo "  停止服务: pkill -f 'python3 app.py'"
fi
echo ""
echo "如需外网访问，请参考《部署指南.md》"
echo ""

