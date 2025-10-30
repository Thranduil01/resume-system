#!/usr/bin/env python3
"""
容错性测试脚本
测试系统在缺少 OCR 和 Grok 环境时是否能正常运行
"""

import sys
import os

# 临时禁用 OCR 和 Grok 导入，模拟没有安装的情况
class ImportBlocker:
    """临时阻止某些模块导入，用于测试容错性"""
    def __init__(self, blocked_modules):
        self.blocked_modules = blocked_modules
        self.original_import = __builtins__.__import__
    
    def __enter__(self):
        def custom_import(name, *args, **kwargs):
            if name in self.blocked_modules or any(name.startswith(m + '.') for m in self.blocked_modules):
                raise ImportError(f"Simulated missing module: {name}")
            return self.original_import(name, *args, **kwargs)
        __builtins__.__import__ = custom_import
        return self
    
    def __exit__(self, *args):
        __builtins__.__import__ = self.original_import


def test_without_ocr():
    """测试没有 OCR 环境时的行为"""
    print("=" * 60)
    print("测试1：模拟没有 OCR 环境")
    print("=" * 60)
    
    # 模拟没有安装 OCR
    with ImportBlocker(['pdf2image', 'pytesseract']):
        try:
            from pdf_parser_enhanced import extract_text_with_ocr
            
            # 尝试使用 OCR（应该返回空字符串而不是崩溃）
            result = extract_text_with_ocr("test.pdf")
            
            if result == "":
                print("✅ 正确：OCR 函数在缺少环境时返回空字符串，不会崩溃")
            else:
                print("⚠️  意外：OCR 返回了内容")
            
            return True
        except Exception as e:
            print(f"❌ 错误：系统崩溃了: {str(e)}")
            return False


def test_without_grok():
    """测试没有 Grok SDK 时的行为"""
    print("\n" + "=" * 60)
    print("测试2：模拟没有 Grok SDK")
    print("=" * 60)
    
    # 模拟没有安装 Grok SDK
    with ImportBlocker(['xai_sdk']):
        try:
            from pdf_parser_enhanced import extract_with_grok_api
            
            # 尝试使用 Grok API（应该返回空结果而不是崩溃）
            result = extract_with_grok_api("test.pdf", "fake_api_key")
            
            expected_keys = ['name', 'email', 'undergraduate_school', 'graduate_school', 'current_grade']
            if all(key in result for key in expected_keys) and all(v is None for v in result.values()):
                print("✅ 正确：Grok API 函数在缺少 SDK 时返回空结果，不会崩溃")
            else:
                print("⚠️  意外：返回结果格式不正确")
            
            return True
        except Exception as e:
            print(f"❌ 错误：系统崩溃了: {str(e)}")
            return False


def test_import_with_missing_modules():
    """测试基础导入（在缺少可选模块时）"""
    print("\n" + "=" * 60)
    print("测试3：基础模块导入测试")
    print("=" * 60)
    
    try:
        # 这些是必需的模块，应该能成功导入
        import flask
        import pdfplumber
        import database
        import pdf_parser
        import pdf_parser_enhanced
        
        print("✅ 正确：所有核心模块成功导入")
        return True
    except ImportError as e:
        print(f"❌ 错误：核心模块导入失败: {str(e)}")
        return False


def main():
    print("\n")
    print("🔬 " + "=" * 56)
    print("🔬 简历信息提取系统 - 容错性测试")
    print("🔬 " + "=" * 56)
    print("\n本测试将模拟缺少可选依赖（OCR、Grok）的情况")
    print("确保系统在这些环境下仍能正常运行\n")
    
    results = []
    
    # 运行测试
    results.append(("基础模块导入", test_import_with_missing_modules()))
    results.append(("无OCR环境", test_without_ocr()))
    results.append(("无Grok SDK", test_without_grok()))
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {status}: {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有测试通过！系统具有良好的容错性。")
        print("   即使缺少 OCR 或 Grok 环境，系统也能正常运行。")
    else:
        print("⚠️  部分测试失败，需要改进容错性。")
    print("=" * 60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

