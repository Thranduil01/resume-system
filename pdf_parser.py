"""
PDF 简历解析器
从 PDF 中提取邮箱、学校、年级等信息
"""
import re
import pdfplumber
from typing import Dict, Set, Optional

# 邮箱正则表达式
EMAIL_RE = re.compile(
    r"[A-Za-z0-9\u4e00-\u9fa5_.+-]+(?:\s*@\s*)"
    r"[A-Za-z0-9-]+(?:\s*\.\s*[A-Za-z0-9-]+)+",
    re.I
)

# 学校关键词（用于识别学校信息）
SCHOOL_KEYWORDS = [
    "大学", "学院", "University", "College", "Institute", "School",
    "本科", "研究生", "硕士", "博士", "undergraduate", "graduate", "master", "phd", "bachelor"
]

# 年级关键词
GRADE_KEYWORDS = [
    "大一", "大二", "大三", "大四",
    "研一", "研二", "研三",
    "博一", "博二", "博三", "博四",
    "本科一年级", "本科二年级", "本科三年级", "本科四年级",
    "硕士一年级", "硕士二年级", "硕士三年级",
    "博士一年级", "博士二年级", "博士三年级", "博士四年级",
    "freshman", "sophomore", "junior", "senior",
    "first year", "second year", "third year", "fourth year"
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
    """
    从文本中提取学校信息
    尝试识别本科学校和研究生学校
    """
    result = {
        "undergraduate_school": None,
        "graduate_school": None
    }
    
    # 将文本按行分割
    lines = text.split('\n')
    
    # 查找包含"本科"的学校
    for i, line in enumerate(lines):
        if "本科" in line or "undergraduate" in line.lower() or "bachelor" in line.lower():
            # 在当前行及前后2行中查找大学名称
            context_lines = lines[max(0, i-2):min(len(lines), i+3)]
            for context_line in context_lines:
                if any(keyword in context_line for keyword in ["大学", "学院", "University", "College"]):
                    # 提取包含大学名称的部分
                    school_match = re.search(r'[\u4e00-\u9fa5A-Za-z\s&]+(?:大学|学院|University|College)', context_line)
                    if school_match:
                        result["undergraduate_school"] = school_match.group(0).strip()
                        break
    
    # 查找包含"研究生"或"硕士"或"博士"的学校
    for i, line in enumerate(lines):
        if any(keyword in line.lower() for keyword in ["研究生", "硕士", "博士", "graduate", "master", "phd"]):
            # 在当前行及前后2行中查找大学名称
            context_lines = lines[max(0, i-2):min(len(lines), i+3)]
            for context_line in context_lines:
                if any(keyword in context_line for keyword in ["大学", "学院", "University", "College"]):
                    # 提取包含大学名称的部分
                    school_match = re.search(r'[\u4e00-\u9fa5A-Za-z\s&]+(?:大学|学院|University|College)', context_line)
                    if school_match:
                        school_name = school_match.group(0).strip()
                        # 如果和本科不同，才设置为研究生学校
                        if school_name != result["undergraduate_school"]:
                            result["graduate_school"] = school_name
                        break
    
    # 如果没有找到明确的本科/研究生标记，尝试找出所有出现的学校
    if not result["undergraduate_school"] and not result["graduate_school"]:
        schools_found = []
        for line in lines:
            school_match = re.search(r'[\u4e00-\u9fa5A-Za-z\s&]+(?:大学|学院|University|College)', line)
            if school_match:
                school_name = school_match.group(0).strip()
                if school_name not in schools_found:
                    schools_found.append(school_name)
        
        # 如果找到学校，将第一个作为本科学校（通常简历会先写本科）
        if schools_found:
            result["undergraduate_school"] = schools_found[0]
            if len(schools_found) > 1:
                result["graduate_school"] = schools_found[1]
    
    return result


def extract_name(text: str) -> Optional[str]:
    """从文本中提取姓名"""
    lines = text.split('\n')
    
    # 常见简历姓名位置：通常在前3行，且较短（2-4个中文字符或英文单词）
    for i, line in enumerate(lines[:5]):  # 只看前5行
        line = line.strip()
        
        # 跳过空行和过长的行
        if not line or len(line) > 20:
            continue
        
        # 中文姓名：2-4个汉字
        chinese_name_match = re.match(r'^[\u4e00-\u9fa5]{2,4}$', line)
        if chinese_name_match:
            return line
        
        # 英文姓名：类似 "Zhang San" 或 "ZHANG SAN"
        english_name_match = re.match(r'^[A-Za-z]+\s+[A-Za-z]+$', line)
        if english_name_match:
            return line
        
        # 检查是否包含"姓名"、"Name"等关键词
        if any(keyword in line for keyword in ["姓名", "Name", "name"]):
            # 尝试提取关键词后面的内容
            name_match = re.search(r'(?:姓名|Name|name)[：:\s]+([\\u4e00-\\u9fa5A-Za-z\s]+)', line)
            if name_match:
                return name_match.group(1).strip()
    
    return None


def extract_grade(text: str) -> Optional[str]:
    """从文本中提取年级信息"""
    # 标准化文本
    text_lower = text.lower()
    
    # 匹配中文年级
    for grade in GRADE_KEYWORDS:
        if grade in text:
            return grade
    
    # 匹配"20XX级"模式
    year_grade_match = re.search(r'(20\d{2})\s*级', text)
    if year_grade_match:
        return f"{year_grade_match.group(1)}级"
    
    # 匹配"大X"或"研X"或"博X"
    grade_match = re.search(r'(大|研|博)([一二三四])', text)
    if grade_match:
        return f"{grade_match.group(1)}{grade_match.group(2)}"
    
    # 匹配英文年级（大写或小写）
    if "freshman" in text_lower:
        return "大一"
    elif "sophomore" in text_lower:
        return "大二"
    elif "junior" in text_lower:
        return "大三"
    elif "senior" in text_lower:
        return "大四"
    
    # 匹配"first/second/third/fourth year" + "undergraduate/graduate"
    year_match = re.search(r'(first|second|third|fourth)\s+year\s*(undergraduate|graduate)?', text_lower)
    if year_match:
        year_map = {"first": "一", "second": "二", "third": "三", "fourth": "四"}
        degree_map = {"undergraduate": "大", "graduate": "研"}
        year_num = year_map.get(year_match.group(1), "")
        degree = degree_map.get(year_match.group(2), "大") if year_match.group(2) else "大"
        return f"{degree}{year_num}"
    
    return None


def parse_pdf(pdf_path: str) -> Dict[str, Optional[str]]:
    """
    解析PDF文件，提取所有需要的信息
    返回字典包含：name, email, undergraduate_school, graduate_school, current_grade
    """
    result = {
        "name": None,
        "email": None,
        "undergraduate_school": None,
        "graduate_school": None,
        "current_grade": None,
        "raw_text": ""
    }
    
    try:
        # 读取PDF文本
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
        
        result["raw_text"] = text
        
        # 提取姓名
        result["name"] = extract_name(text)
        
        # 提取邮箱（取第一个）
        emails = extract_emails(text)
        if emails:
            result["email"] = sorted(emails)[0]  # 取第一个邮箱
        
        # 提取学校信息
        schools = extract_schools(text)
        result["undergraduate_school"] = schools["undergraduate_school"]
        result["graduate_school"] = schools["graduate_school"]
        
        # 提取年级
        result["current_grade"] = extract_grade(text)
        
    except Exception as e:
        print(f"解析PDF时出错 {pdf_path}: {str(e)}")
    
    return result


def parse_multiple_pdfs(pdf_paths: list) -> list:
    """
    批量解析多个PDF文件
    返回解析结果列表
    """
    results = []
    for pdf_path in pdf_paths:
        result = parse_pdf(pdf_path)
        result["filename"] = pdf_path
        results.append(result)
    
    return results


