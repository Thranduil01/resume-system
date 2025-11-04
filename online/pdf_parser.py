"""
PDF 简历解析器
从 PDF 中提取邮箱、学校、年级等信息
优化版：增强邮箱、学校和年级识别能力
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
    """从文本中提取邮箱 - 增强版（支持残缺邮箱修复）"""
    # 多种邮箱格式支持
    email_patterns = [
        # 标准邮箱格式
        r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}',
        # 支持中文字符的邮箱
        r'[\u4e00-\u9fa5A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}',
        # 支持空格的邮箱（PDF提取可能带空格）
        r'[A-Za-z0-9._%+-]+\s*@\s*[A-Za-z0-9.-]+\s*\.\s*[A-Z|a-z]{2,}'
    ]
    
    emails = set()
    for pattern in email_patterns:
        matches = re.findall(pattern, text, re.I)
        for match in matches:
            # 清理邮箱中的空格和特殊字符
            email = match.replace(" ", "").replace("\n", "").replace("\t", "")
            # 验证邮箱格式
            if '@' in email and '.' in email.split('@')[1]:
                emails.add(email)
    
    # 特殊处理：修复残缺的邮箱（如 "@qq.com"）
    # 尝试从QQ号推断完整邮箱
    if not emails and '@qq.com' in text.lower():
        # 查找QQ号
        qq_matches = re.findall(r'QQ[：:\s]*(\d{5,12})', text, re.I)
        if qq_matches:
            # 使用找到的QQ号构建完整邮箱
            qq_num = qq_matches[0]
            emails.add(f"{qq_num}@qq.com")
            print(f"  💡 从QQ号修复邮箱: {qq_num}@qq.com")
        else:
            # 尝试查找纯数字QQ号
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if 'qq' in line.lower() or '邮箱' in line:
                    # 在前后3行寻找数字
                    for j in range(max(0, i-3), min(len(lines), i+4)):
                        digits = re.findall(r'\b(\d{5,12})\b', lines[j])
                        if digits:
                            qq_num = digits[0]
                            emails.add(f"{qq_num}@qq.com")
                            print(f"  💡 从附近数字推断QQ邮箱: {qq_num}@qq.com")
                            break
                    if emails:
                        break
    
    # 特殊处理：修复其他残缺邮箱
    if not emails:
        # 查找 @domain.com 格式并尝试从其他信息补全
        incomplete_email = re.search(r'@(qq|163|126|outlook|gmail)\.(com|cn)', text, re.I)
        if incomplete_email:
            domain = incomplete_email.group(0)
            # 查找可能的用户名（手机号、学号等）
            possible_usernames = re.findall(r'\b(\d{5,15})\b', text)
            if possible_usernames:
                # 使用第一个看起来合理的数字
                for username in possible_usernames:
                    if len(username) >= 6:  # 合理的邮箱用户名长度
                        email = f"{username}{domain}"
                        emails.add(email)
                        print(f"  💡 修复残缺邮箱: {email}")
                        break
    
    return emails


def extract_schools(text: str) -> Dict[str, Optional[str]]:
    """
    从文本中提取学校信息 - 增强版
    智能识别本科学校和研究生学校（支持根据时间判断）
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
    
    # 如果没有找到明确的本科/研究生标记，尝试根据时间智能识别
    if not result["undergraduate_school"] and not result["graduate_school"]:
        schools_with_dates = []
        for i, line in enumerate(lines):
            # 匹配学校名称
            school_match = re.search(r'([\u4e00-\u9fa5A-Za-z\s&]+(?:大学|学院|University|College))', line)
            if school_match:
                school_name = school_match.group(1).strip()
                # 尝试找到相关的时间信息（前后3行内）
                date_info = ""
                for j in range(max(0, i-3), min(len(lines), i+4)):
                    # 匹配时间格式：2022.9-2026.6 或 2022-2026 等
                    date_match = re.search(r'(20\d{2}[\.\-/]?\d{0,2}[\s\-～~到至]*20\d{2}[\.\-/]?\d{0,2})', lines[j])
                    if date_match:
                        date_info = date_match.group(1)
                        break
                
                # 避免重复添加
                if school_name not in [s[0] for s in schools_with_dates]:
                    schools_with_dates.append((school_name, date_info))
        
        # 根据时间判断本科和研究生
        if schools_with_dates:
            # 按时间排序（早的优先）
            schools_with_dates.sort(key=lambda x: x[1] if x[1] else "9999")
            
            # 第一个通常是本科
            result["undergraduate_school"] = schools_with_dates[0][0]
            
            # 如果有第二个，判断是否是研究生
            if len(schools_with_dates) > 1:
                second_date = schools_with_dates[1][1]
                # 如果时间包含2026年或更晚，很可能是研究生
                if second_date and any(year in second_date for year in ['2026', '2027', '2028', '2029', '2030']):
                    result["graduate_school"] = schools_with_dates[1][0]
                elif schools_with_dates[1][0] != result["undergraduate_school"]:
                    result["graduate_school"] = schools_with_dates[1][0]
    
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
            name_match = re.search(r'(?:姓名|Name|name)[：:\s]+([\u4e00-\u9fa5A-Za-z\s]+)', line)
            if name_match:
                return name_match.group(1).strip()
    
    return None


def extract_grade(text: str) -> Optional[str]:
    """从文本中提取年级信息 - 增强版（支持根据时间推断）"""
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
    
    # 根据入学时间推断年级（新增功能）
    date_match = re.search(r'(20\d{2})[\.\-/]?\d{0,2}[\s\-～~到至]*(20\d{2})[\.\-/]?\d{0,2}', text)
    if date_match:
        start_year = int(date_match.group(1))
        end_year = int(date_match.group(2))
        duration = end_year - start_year
        
        # 根据当前年份推断年级
        current_year = 2025
        years_passed = current_year - start_year
        
        # 4年制本科
        if duration == 4 and 0 < years_passed <= 4:
            grade_map = {1: "大一", 2: "大二", 3: "大三", 4: "大四"}
            return grade_map.get(years_passed, f"大{years_passed}")
        
        # 2-3年制研究生
        elif duration <= 3 and end_year >= 2026:
            if years_passed <= 0:
                return "研一"  # 还未入学或刚入学
            elif years_passed == 1:
                return "研二"
            elif years_passed == 2:
                return "研三"
    
    # 匹配英文年级
    if "freshman" in text_lower:
        return "大一"
    elif "sophomore" in text_lower:
        return "大二"
    elif "junior" in text_lower:
        return "大三"
    elif "senior" in text_lower:
        return "大四"
    
    # 匹配"first/second/third/fourth year"
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
