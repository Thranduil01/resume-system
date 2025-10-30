#!/usr/bin/env python3
"""
测试单个 PDF 文件的识别效果
使用方法：python3 test_single_pdf.py "pdf test/李美霖+简历.pdf"
"""

import sys
import os

def test_pdf(pdf_path):
    """测试PDF识别"""
    if not os.path.exists(pdf_path):
        print(f"❌ 文件不存在: {pdf_path}")
        return
    
    print(f"📄 测试文件: {pdf_path}")
    print("=" * 60)
    
    # 第一级：文本提取
    print("\n🔍 第一级：文本提取测试")
    print("-" * 60)
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            
            if text.strip():
                print(f"✅ 成功提取文本，长度: {len(text)} 字符")
                print(f"前 200 字符:\n{text[:200]}")
                
                # 检查邮箱
                import re
                emails = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', text)
                if emails:
                    print(f"\n📧 找到邮箱: {emails}")
            else:
                print("⚠️ 未提取到文本（可能是扫描版PDF）")
    except Exception as e:
        print(f"❌ 文本提取失败: {str(e)}")
    
    # 第二级：OCR 识别
    print("\n\n🔍 第二级：OCR 识别测试")
    print("-" * 60)
    try:
        from pdf2image import convert_from_path
        import pytesseract
        
        print("📸 正在将 PDF 转换为图片...")
        images = convert_from_path(pdf_path, dpi=300, first_page=1, last_page=1)
        
        if images:
            print(f"✅ 成功转换，共 {len(images)} 张图片")
            print("🔍 正在进行 OCR 识别（中英文混合）...")
            
            ocr_text = pytesseract.image_to_string(images[0], lang='chi_sim+eng')
            
            if ocr_text.strip():
                print(f"✅ OCR 识别成功，长度: {len(ocr_text)} 字符")
                print(f"\n识别结果（前 500 字符）:\n")
                print(ocr_text[:500])
                
                # 检查邮箱
                import re
                emails = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}', ocr_text)
                if emails:
                    print(f"\n📧 OCR 找到邮箱: {emails}")
                else:
                    print("\n⚠️ OCR 未识别到邮箱")
            else:
                print("⚠️ OCR 识别结果为空")
        else:
            print("❌ PDF 转图片失败")
            
    except ImportError as e:
        print(f"❌ OCR 功能不可用（缺少依赖）: {str(e)}")
        print("\n请安装:")
        print("  1. Tesseract OCR: brew install tesseract tesseract-lang")
        print("  2. Poppler: brew install poppler")
    except Exception as e:
        print(f"❌ OCR 识别失败: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        test_path = "pdf test/李美霖+简历.pdf"
        print(f"使用默认路径: {test_path}")
    else:
        test_path = sys.argv[1]
    
    test_pdf(test_path)

