#!/bin/bash
# 快速安装 OCR 所需软件

echo "================================"
echo "开始安装 OCR 环境"
echo "================================"

# 检查 Homebrew
if ! command -v brew &> /dev/null; then
    echo "❌ 未检测到 Homebrew"
    echo "请先安装 Homebrew："
    echo ""
    echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    echo ""
    exit 1
fi

echo "✓ Homebrew 已安装"
echo ""

# 安装 Tesseract
echo "📦 安装 Tesseract OCR..."
brew install tesseract

# 安装中文语言包
echo "📦 安装中文语言包..."
brew install tesseract-lang

# 安装 Poppler
echo "📦 安装 Poppler..."
brew install poppler

echo ""
echo "================================"
echo "安装完成！验证安装..."
echo "================================"

# 验证
if command -v tesseract &> /dev/null; then
    echo "✅ Tesseract OCR: $(tesseract --version | head -1)"
else
    echo "❌ Tesseract OCR 安装失败"
fi

if command -v pdfinfo &> /dev/null; then
    echo "✅ Poppler: $(pdfinfo -v 2>&1 | head -1)"
else
    echo "❌ Poppler 安装失败"
fi

echo ""
echo "================================"
echo "🎉 安装完成！"
echo "现在可以使用 OCR 功能了"
echo "================================"

