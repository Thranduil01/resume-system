# OCR 功能安装指南

## 📦 安装 Tesseract OCR

OCR 功能需要安装 Tesseract OCR 引擎。以下是不同系统的安装方法：

### macOS

```bash
# 使用 Homebrew 安装
brew install tesseract
brew install tesseract-lang  # 安装语言包（包含中文）

# 或者只安装中文语言包
brew install tesseract
brew install tesseract-lang-chi-sim  # 简体中文
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-chi-sim  # 简体中文语言包
```

### Windows

1. 下载安装程序：https://github.com/UB-Mannheim/tesseract/wiki
2. 运行安装程序，确保选择中文语言包
3. 将 Tesseract 路径添加到系统环境变量

或使用 Chocolatey：
```powershell
choco install tesseract
```

## 🔧 验证安装

安装完成后，验证 Tesseract 是否安装成功：

```bash
tesseract --version
```

应该看到类似输出：
```
tesseract 5.x.x
```

## 📚 安装 Python 依赖

```bash
pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org pdf2image pytesseract Pillow requests
```

## 🖼️ 安装 Poppler（pdf2image 需要）

### macOS
```bash
brew install poppler
```

### Linux (Ubuntu/Debian)
```bash
sudo apt install poppler-utils
```

### Windows
1. 下载 Poppler：http://blog.alivate.com.au/poppler-windows/
2. 解压到某个目录（如 C:\Program Files\poppler）
3. 将 bin 目录添加到系统环境变量

## ✅ 完整安装流程（macOS）

```bash
# 1. 安装 Tesseract OCR 和语言包
brew install tesseract tesseract-lang

# 2. 安装 Poppler
brew install poppler

# 3. 安装 Python 依赖
cd "/Users/zhanghan5/Downloads/6. coding/1030 intern_email_address"
pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# 4. 验证安装
tesseract --version
pdfinfo -v
```

## 🎯 测试 OCR 功能

安装完成后：
1. 启动服务器：`python3 app.py`
2. 打开浏览器：`http://127.0.0.1:5001`
3. 勾选"启用 OCR 识别"选项
4. 解析包含扫描版 PDF 的文件夹

## ❗常见问题

### Q1: pytesseract.TesseractNotFoundError
**A**: Tesseract 未安装或未添加到系统路径。请重新安装 Tesseract。

对于 macOS，可以在代码中指定路径：
```python
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
```

### Q2: pdf2image 报错找不到 Poppler
**A**: 需要安装 Poppler。macOS 使用 `brew install poppler`。

### Q3: OCR 识别效果不好
**A**: 
- 确保安装了中文语言包
- 提高 PDF 转图片的 DPI（在代码中调整 dpi 参数）
- 对图片进行预处理（二值化、去噪等）

## 🚀 无需安装 OCR 的替代方案

如果不想安装 OCR，可以：
1. 取消勾选"启用 OCR 识别"
2. 使用 **Grok API** 进行智能识别（更强大，不需要本地 OCR）
   - 在网页中输入 Grok API Key
   - 系统会自动使用 AI 视觉模型识别简历

