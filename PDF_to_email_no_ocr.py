"""
批量提取 PDF 中的邮箱（无 OCR 版）：
1. 只用 pdfplumber 解析文字
2. 如果没抓到邮箱 ➜ 记录为未提取到邮箱
结果：在同一文件夹生成
  - YYYYMMDD_HHMMSS_emails.txt      所有唯一邮箱，用 "; " 分隔
  - YYYYMMDD_HHMMSS_no_email.txt    未提取到邮箱的 PDF 文件名
  - YYYYMMDD_HHMMSS_extract_log.csv  过程记录，含文件名、邮箱、提取方法
依赖：pip install pdfplumber
"""

import os, re, sys, csv
from datetime import datetime
import pdfplumber

EMAIL_RE = re.compile(
    r"[A-Za-z0-9\u4e00-\u9fa5_.+-]+(?:\s*@\s*)"
    r"[A-Za-z0-9-]+(?:\s*\.\s*[A-Za-z0-9-]+)+",
    re.I
)

def extract_emails(text):
    text = re.sub(r"\s+", " ", text)
    raw = EMAIL_RE.findall(text)
    return {
        re.sub(r"^[\s\|丨/\\,;:]+|[\s\|丨/\\,;:]+$", "", re.sub(r"\s+", "", m))
        for m in raw
    }

def extract_from_pdf(path):
    """只用 pdfplumber 解析，不做 OCR"""
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    emails = extract_emails(text)
    if emails:
        return emails, "文本解析"
    else:
        return set(), "未提取到邮箱"

def main(folder):
    all_emails, no_email = set(), []
    records = []  # 记录每个文件的提取情况
    for fn in os.listdir(folder):
        if fn.lower().endswith(".pdf"):
            fp = os.path.join(folder, fn)
            emails, method = extract_from_pdf(fp)
            if emails:
                all_emails.update(emails)
                records.append([fn, "; ".join(sorted(emails)), method])
            else:
                no_email.append(fn)
                records.append([fn, "", "未提取到邮箱"])

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    email_file = os.path.join(folder, f"{ts}_emails.txt")
    no_file = os.path.join(folder, f"{ts}_no_email.txt")
    csv_file = os.path.join(folder, f"{ts}_extract_log.csv")

    with open(email_file, "w", encoding="utf-8") as f:
        f.write("; ".join(sorted(all_emails)))
    with open(no_file, "w", encoding="utf-8") as f:
        f.write("\n".join(no_email))
    with open(csv_file, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["文件标题", "邮箱", "提取方法"])
        writer.writerows(records)

    print(f"✅ 提取 {len(all_emails)} 个邮箱 → {email_file}")
    print(f"❗未提取到邮箱的 PDF 共 {len(no_email)} 个 → {no_file}")
    print(f"📄 过程记录已保存为 → {csv_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python extract_emails_no_ocr.py <pdf_folder>")
    else:
        folder = sys.argv[1]
        if os.path.isdir(folder):
            main(folder)
        else:
            print("❗ 路径无效") 