"""
增强版 PDF 简历解析器
支持三级识别：文本提取 -> OCR -> Grok API
"""
import re
import pdfplumber
from typing import Dict, Set, Optional, Tuple
import os
import json
import requests

# OCR 相关的导入延迟到使用时（避免部署时缺少依赖报错）
# from pdf2image import convert_from_path
# import pytesseract
# from PIL import Image

# 从基础解析器导入函数
from pdf_parser import extract_name

# 邮箱正则表达式
EMAIL_RE = re.compile(
    r"[A-Za-z0-9\u4e00-\u9fa5_.+-]+(?:\s*@\s*)"
    r"[A-Za-z0-9-]+(?:\s*\.\s*[A-Za-z0-9-]+)+",
    re.I
)

# 学校关键词
SCHOOL_KEYWORDS = [
    "大学", "学院", "University", "College", "Institute", "School"
]

# 年级关键词
GRADE_KEYWORDS = [
    "大一", "大二", "大三", "大四",
    "研一", "研二", "研三",
    "博一", "博二", "博三", "博四",
    "本科一年级", "本科二年级", "本科三年级", "本科四年级",
    "硕士一年级", "硕士二年级", "硕士三年级",
    "博士一年级", "博士二年级", "博士三年级", "博士四年级",
    "freshman", "sophomore", "junior", "senior"
]


def extract_emails(text: str) -> Set[str]:
    """从文本中提取邮箱"""
    text = re.sub(r"\s+", " ", text)
    raw = EMAIL_RE.findall(text)
    return {
        re.sub(r"^[\s\|丨/\\,;:]+|[\s\|丨/\\,;:]+$", "", re.sub(r"\s+", "", m))
        for m in raw
    }


def extract_schools(text: str) -> Dict[str, Optional[str]]:
    """从文本中提取学校信息"""
    result = {
        "undergraduate_school": None,
        "graduate_school": None
    }
    
    lines = text.split('\n')
    
    # 查找本科学校
    for i, line in enumerate(lines):
        if "本科" in line or "undergraduate" in line.lower() or "bachelor" in line.lower():
            context_lines = lines[max(0, i-2):min(len(lines), i+3)]
            for context_line in context_lines:
                if any(keyword in context_line for keyword in ["大学", "学院", "University", "College"]):
                    school_match = re.search(r'[\u4e00-\u9fa5A-Za-z\s&]+(?:大学|学院|University|College)', context_line)
                    if school_match:
                        result["undergraduate_school"] = school_match.group(0).strip()
                        break
    
    # 查找研究生学校
    for i, line in enumerate(lines):
        if any(keyword in line.lower() for keyword in ["研究生", "硕士", "博士", "graduate", "master", "phd"]):
            context_lines = lines[max(0, i-2):min(len(lines), i+3)]
            for context_line in context_lines:
                if any(keyword in context_line for keyword in ["大学", "学院", "University", "College"]):
                    school_match = re.search(r'[\u4e00-\u9fa5A-Za-z\s&]+(?:大学|学院|University|College)', context_line)
                    if school_match:
                        school_name = school_match.group(0).strip()
                        if school_name != result["undergraduate_school"]:
                            result["graduate_school"] = school_name
                        break
    
    # 如果没有明确标记，尝试找出所有学校
    if not result["undergraduate_school"] and not result["graduate_school"]:
        schools_found = []
        for line in lines:
            school_match = re.search(r'[\u4e00-\u9fa5A-Za-z\s&]+(?:大学|学院|University|College)', line)
            if school_match:
                school_name = school_match.group(0).strip()
                if school_name not in schools_found:
                    schools_found.append(school_name)
        
        if schools_found:
            result["undergraduate_school"] = schools_found[0]
            if len(schools_found) > 1:
                result["graduate_school"] = schools_found[1]
    
    return result


def extract_grade(text: str) -> Optional[str]:
    """从文本中提取年级信息"""
    text_lower = text.lower()
    
    for grade in GRADE_KEYWORDS:
        if grade in text:
            return grade
    
    year_grade_match = re.search(r'(20\d{2})\s*级', text)
    if year_grade_match:
        return f"{year_grade_match.group(1)}级"
    
    grade_match = re.search(r'(大|研|博)([一二三四])', text)
    if grade_match:
        return f"{grade_match.group(1)}{grade_match.group(2)}"
    
    if "freshman" in text_lower:
        return "大一"
    elif "sophomore" in text_lower:
        return "大二"
    elif "junior" in text_lower:
        return "大三"
    elif "senior" in text_lower:
        return "大四"
    
    year_match = re.search(r'(first|second|third|fourth)\s+year\s*(undergraduate|graduate)?', text_lower)
    if year_match:
        year_map = {"first": "一", "second": "二", "third": "三", "fourth": "四"}
        degree_map = {"undergraduate": "大", "graduate": "研"}
        year_num = year_map.get(year_match.group(1), "")
        degree = degree_map.get(year_match.group(2), "大") if year_match.group(2) else "大"
        return f"{degree}{year_num}"
    
    return None


def extract_text_from_pdf(pdf_path: str) -> str:
    """第一级：使用 pdfplumber 提取文本"""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
    except Exception as e:
        print(f"文本提取失败: {str(e)}")
    return text


def extract_text_with_ocr(pdf_path: str) -> str:
    """第二级：使用 OCR 提取文本"""
    text = ""
    try:
        # 检查是否安装了必要的OCR工具
        try:
            from pdf2image import convert_from_path
            import pytesseract
        except ImportError as e:
            print(f"⚠️ OCR 环境未安装，跳过 OCR 识别")
            print(f"   提示：如需使用 OCR，请安装：pip install pdf2image pytesseract")
            return text
        
        # 检查 Tesseract 是否可用
        try:
            pytesseract.get_tesseract_version()
        except Exception:
            print(f"⚠️ Tesseract OCR 未安装，跳过 OCR 识别")
            print(f"   提示：请安装 Tesseract OCR（macOS: brew install tesseract tesseract-lang poppler）")
            return text
        
        # 将 PDF 转换为图片
        images = convert_from_path(pdf_path, dpi=300, first_page=1, last_page=3)  # 只处理前3页
        
        # 对每张图片进行 OCR
        for i, image in enumerate(images):
            # 使用中英文混合识别
            ocr_text = pytesseract.image_to_string(image, lang='chi_sim+eng')
            text += ocr_text + "\n"
            print(f"OCR 处理第 {i+1} 页完成")
        
    except Exception as e:
        print(f"⚠️ OCR 识别失败: {str(e)}")
        print(f"   文件 {os.path.basename(pdf_path)} 将使用其他方法识别")
    
    return text


def extract_with_grok_api(pdf_path: str, api_key: str) -> Dict[str, Optional[str]]:
    """
    第三级：使用 Grok API 智能提取信息（使用官方 SDK）
    需要提供 Grok API Key
    """
    result = {
        "name": None,
        "email": None,
        "undergraduate_school": None,
        "graduate_school": None,
        "current_grade": None
    }
    
    try:
        # 检查是否安装了 xai-sdk
        try:
            from xai_sdk import Client
            from xai_sdk.chat import user, image as sdk_image
        except ImportError:
            print(f"⚠️ Grok SDK 未安装，跳过 Grok API 识别")
            print(f"   提示：如需使用 Grok API，请安装：pip install xai-sdk")
            return result
        # 使用 PyMuPDF 将 PDF 转换为图片（只取第一页）
        import fitz
        from PIL import Image
        import io
        
        pdf_document = fitz.open(pdf_path)
        page = pdf_document[0]
        mat = fitz.Matrix(1.5, 1.5)  # 150 DPI
        pix = page.get_pixmap(matrix=mat)
        img_data = pix.tobytes("jpeg")
        image = Image.open(io.BytesIO(img_data))
        pdf_document.close()
        
        images = [image]
        
        if not images:
            return result
        
        # 保存临时图片
        temp_image_path = "/tmp/resume_temp.jpg"
        images[0].save(temp_image_path, "JPEG", quality=85, optimize=True)
        
        # 使用 Grok 官方 SDK
        from xai_sdk import Client
        from xai_sdk.chat import user, image as sdk_image
        import base64
        
        # 编码图片为 base64
        with open(temp_image_path, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        
        # 创建客户端
        client = Client(api_key=api_key)
        chat = client.chat.create(model="grok-4-fast-non-reasoning")
        
        prompt = """请从这份简历图片中提取以下信息，以JSON格式返回：
{
    "name": "学生姓名",
    "email": "邮箱地址",
    "undergraduate_school": "本科学校名称",
    "graduate_school": "研究生学校名称（如果有）",
    "current_grade": "当前年级（如：大三、研一等）"
}

如果某个信息找不到，请返回 null。
只返回JSON，不要其他内容。"""
        
        # 添加消息并发送请求
        chat.append(
            user(
                prompt,
                sdk_image(image_url=f"data:image/jpeg;base64,{image_base64}", detail="high"),
            )
        )
        
        response = chat.sample()
        content = response.content
        
        # 尝试解析 JSON
        try:
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                extracted_data = json.loads(json_match.group(0))
                result.update(extracted_data)
        except json.JSONDecodeError:
            print("无法解析 Grok API 返回的 JSON")
        
        # 清理临时文件
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)
            
    except Exception as e:
        print(f"⚠️ Grok API 调用出错: {str(e)}")
        print(f"   文件 {os.path.basename(pdf_path)} 的 AI 识别失败，将使用已提取的信息")
    
    return result


def parse_pdf_enhanced(pdf_path: str, use_ocr: bool = True, grok_api_key: Optional[str] = None) -> Tuple[Dict[str, Optional[str]], str]:
    """
    增强版 PDF 解析，支持三级识别
    
    Args:
        pdf_path: PDF 文件路径
        use_ocr: 是否启用 OCR（当文本提取失败时）
        grok_api_key: Grok API Key（可选，用于第三级识别）
    
    Returns:
        (result_dict, method_used)
    """
    result = {
        "name": None,
        "email": None,
        "undergraduate_school": None,
        "graduate_school": None,
        "current_grade": None,
        "raw_text": ""
    }
    
    method_used = "未提取到信息"
    
    # 第一级：普通文本提取
    print(f"正在处理: {os.path.basename(pdf_path)}")
    text = extract_text_from_pdf(pdf_path)
    result["raw_text"] = text
    
    if text.strip():
        result["name"] = extract_name(text)
        
        emails = extract_emails(text)
        if emails:
            result["email"] = sorted(emails)[0]
        
        schools = extract_schools(text)
        result["undergraduate_school"] = schools["undergraduate_school"]
        result["graduate_school"] = schools["graduate_school"]
        result["current_grade"] = extract_grade(text)
        
        # 检查是否提取到关键信息
        if result["email"] or result["undergraduate_school"] or result["current_grade"]:
            method_used = "文本提取"
            print(f"✓ 文本提取成功")
            return result, method_used
    
    # 第二级：OCR 识别
    if use_ocr:
        print(f"文本提取未获取完整信息，尝试 OCR 识别...")
        try:
            ocr_text = extract_text_with_ocr(pdf_path)
            result["raw_text"] += "\n" + ocr_text
            
            if ocr_text.strip():
                if not result["name"]:
                    result["name"] = extract_name(ocr_text)
                
                emails = extract_emails(ocr_text)
                if emails and not result["email"]:
                    result["email"] = sorted(emails)[0]
                
                schools = extract_schools(ocr_text)
                if not result["undergraduate_school"]:
                    result["undergraduate_school"] = schools["undergraduate_school"]
                if not result["graduate_school"]:
                    result["graduate_school"] = schools["graduate_school"]
                
                if not result["current_grade"]:
                    result["current_grade"] = extract_grade(ocr_text)
                
                if result["email"] or result["undergraduate_school"] or result["current_grade"]:
                    method_used = "OCR识别"
                    print(f"✓ OCR 识别成功")
                    return result, method_used
        except Exception as e:
            print(f"OCR 识别出错: {str(e)}")
    
    # 第三级：Grok API 智能识别
    if grok_api_key:
        print(f"OCR 识别未获取完整信息，尝试 Grok API 智能识别...")
        try:
            grok_result = extract_with_grok_api(pdf_path, grok_api_key)
            
            # 合并结果（优先使用 Grok 的结果）
            if grok_result["name"] and not result["name"]:
                result["name"] = grok_result["name"]
            if grok_result["email"] and not result["email"]:
                result["email"] = grok_result["email"]
            if grok_result["undergraduate_school"] and not result["undergraduate_school"]:
                result["undergraduate_school"] = grok_result["undergraduate_school"]
            if grok_result["graduate_school"] and not result["graduate_school"]:
                result["graduate_school"] = grok_result["graduate_school"]
            if grok_result["current_grade"] and not result["current_grade"]:
                result["current_grade"] = grok_result["current_grade"]
            
            if result["email"] or result["undergraduate_school"] or result["current_grade"]:
                method_used = "Grok API 智能识别"
                print(f"✓ Grok API 识别成功")
        except Exception as e:
            print(f"Grok API 识别出错: {str(e)}")
    
    if method_used == "未提取到信息":
        print(f"✗ 所有方法均未能提取到完整信息")
    
    return result, method_used


def parse_multiple_pdfs_enhanced(pdf_paths: list, use_ocr: bool = True, grok_api_key: Optional[str] = None) -> list:
    """批量解析多个 PDF 文件（增强版）"""
    results = []
    for pdf_path in pdf_paths:
        result, method = parse_pdf_enhanced(pdf_path, use_ocr, grok_api_key)
        result["filename"] = os.path.basename(pdf_path)
        result["extraction_method"] = method
        results.append(result)
    
    return results

