#!/usr/bin/env python3
"""
环境检测脚本
检查系统是否安装了必要的依赖
"""

def check_environment():
    """检查系统环境"""
    print("=" * 60)
    print("📋 简历信息提取系统 - 环境检测")
    print("=" * 60)
    
    # 基础Python库检测
    print("\n【基础环境检测】")
    
    required_packages = [
        ("Flask", "flask"),
        ("pdfplumber", "pdfplumber"),
        ("Pillow", "PIL"),
        ("PyMuPDF", "fitz"),
    ]
    
    missing_basic = []
    for name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"  ✅ {name}: 已安装")
        except ImportError:
            print(f"  ❌ {name}: 未安装")
            missing_basic.append(name)
    
    # OCR环境检测
    print("\n【OCR 环境检测】(可选)")
    ocr_available = True
    
    # 检查 pdf2image
    try:
        import pdf2image
        print(f"  ✅ pdf2image: 已安装")
    except ImportError:
        print(f"  ❌ pdf2image: 未安装")
        ocr_available = False
    
    # 检查 pytesseract
    try:
        import pytesseract
        print(f"  ✅ pytesseract: 已安装")
        
        # 检查 Tesseract 可执行文件
        try:
            version = pytesseract.get_tesseract_version()
            print(f"  ✅ Tesseract OCR: 已安装 (版本 {version})")
        except Exception as e:
            print(f"  ❌ Tesseract OCR: 未安装（命令行工具）")
            print(f"     提示: macOS 使用 'brew install tesseract tesseract-lang'")
            ocr_available = False
    except ImportError:
        print(f"  ❌ pytesseract: 未安装")
        ocr_available = False
    
    # 检查 Poppler (pdfinfo)
    import subprocess
    try:
        result = subprocess.run(['pdfinfo', '-v'], capture_output=True, timeout=2)
        if result.returncode == 0:
            print(f"  ✅ Poppler (pdfinfo): 已安装")
        else:
            print(f"  ❌ Poppler (pdfinfo): 未找到")
            print(f"     提示: macOS 使用 'brew install poppler'")
            ocr_available = False
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print(f"  ❌ Poppler (pdfinfo): 未安装")
        print(f"     提示: macOS 使用 'brew install poppler'")
        ocr_available = False
    
    # Grok API 检测
    print("\n【Grok API 环境检测】(可选)")
    grok_available = True
    
    try:
        import xai_sdk
        print(f"  ✅ xai-sdk: 已安装")
    except ImportError:
        print(f"  ❌ xai-sdk: 未安装")
        print(f"     提示: pip install xai-sdk")
        grok_available = False
    
    # 总结
    print("\n" + "=" * 60)
    print("【环境检测总结】")
    print("=" * 60)
    
    if missing_basic:
        print(f"\n❌ 基础环境不完整，缺少: {', '.join(missing_basic)}")
        print(f"   安装命令: pip install {' '.join(missing_basic.lower())}")
        print(f"\n⚠️  系统无法正常运行，请先安装基础依赖！")
    else:
        print(f"\n✅ 基础环境: 完整")
        print(f"   ✔️ 系统可以正常运行（仅文本提取功能）")
    
    if ocr_available:
        print(f"\n✅ OCR 环境: 已安装")
        print(f"   ✔️ 可以识别扫描版 PDF")
    else:
        print(f"\n⚠️  OCR 环境: 未完整安装")
        print(f"   ⚠️  无法识别扫描版 PDF（仅能处理文本型 PDF）")
        print(f"\n   安装方法:")
        print(f"   1. pip install pdf2image pytesseract")
        print(f"   2. brew install tesseract tesseract-lang poppler  (macOS)")
    
    if grok_available:
        print(f"\n✅ Grok API: SDK 已安装")
        print(f"   ✔️ 可以使用 AI 智能识别（需要 API Key）")
    else:
        print(f"\n⚠️  Grok API: SDK 未安装")
        print(f"   ⚠️  无法使用 AI 智能识别")
        print(f"\n   安装方法: pip install xai-sdk")
    
    print("\n" + "=" * 60)
    print("【推荐配置】")
    print("=" * 60)
    print("\n最小配置（仅文本型 PDF）:")
    print("  - Flask, pdfplumber, Pillow, PyMuPDF")
    print("\n推荐配置（支持扫描版 PDF）:")
    print("  - 最小配置 + OCR 环境")
    print("\n完整配置（最强大）:")
    print("  - 推荐配置 + Grok API SDK + API Key")
    
    print("\n" + "=" * 60)
    
    # 返回状态
    return {
        "basic": len(missing_basic) == 0,
        "ocr": ocr_available,
        "grok": grok_available
    }

if __name__ == "__main__":
    status = check_environment()
    
    # 退出码
    if not status["basic"]:
        exit(1)  # 基础环境缺失
    else:
        exit(0)  # 基础环境完整，可以运行

