# 📤 部署和分享指南

## 🎯 分享给别人使用的最佳实践

### 方案1：最简单（推荐给非技术用户）⭐

打包以下文件发给对方：

```
📦 简历提取系统/
├── app.py                    # 主程序
├── database.py               # 数据库
├── pdf_parser.py             # PDF解析
├── pdf_parser_enhanced.py    # 增强解析
├── check_environment.py      # 环境检测 ⭐
├── requirements-minimal.txt  # 最小依赖 ⭐
├── requirements-ocr.txt      # OCR依赖（可选）
├── requirements-grok.txt     # Grok依赖（可选）
├── requirements.txt          # 完整依赖
├── templates/
│   └── index.html           # 网页界面
├── README.md                # 使用说明
└── DEPLOYMENT.md            # 本文件
```

#### 对方操作步骤（3步）：

```bash
# 1. 环境检测（推荐先运行）
python3 check_environment.py

# 2. 安装最小依赖（5秒）
pip3 install -r requirements-minimal.txt

# 3. 启动系统
python3 app.py
```

访问：http://127.0.0.1:5001

---

### 方案2：完整功能（推荐给技术用户）

```bash
# 1. 检查环境
python3 check_environment.py

# 2. 安装Python依赖
pip3 install -r requirements-minimal.txt
pip3 install -r requirements-ocr.txt

# 3. 安装系统依赖（macOS）
brew install tesseract tesseract-lang poppler

# 4. 启动
python3 app.py
```

---

## ✅ 容错性保证

### 不会报错的情况：

1. **没有安装 OCR**
   - ✅ 系统正常运行
   - ⚠️ 提示："OCR 环境未安装，跳过 OCR 识别"
   - ✅ 仍然可以处理文本型 PDF

2. **没有安装 Grok SDK**
   - ✅ 系统正常运行
   - ⚠️ 提示："Grok SDK 未安装，跳过 Grok API 识别"
   - ✅ 使用文本提取或 OCR

3. **没有提供 Grok API Key**
   - ✅ 系统正常运行
   - ⚠️ 不会调用 Grok API
   - ✅ 使用文本提取或 OCR

4. **某个 PDF 无法识别**
   - ✅ 系统继续处理其他文件
   - ⚠️ 在结果中标记为"未提取到信息"
   - ✅ 不会中断整个批处理

---

## 🔍 用户环境检测

### 自动检测脚本

运行 `check_environment.py` 会显示：

```
============================================================
📋 简历信息提取系统 - 环境检测
============================================================

【基础环境检测】
  ✅ Flask: 已安装
  ✅ pdfplumber: 已安装
  ✅ Pillow: 已安装
  ✅ PyMuPDF: 已安装

【OCR 环境检测】(可选)
  ❌ pdf2image: 未安装
  ❌ pytesseract: 未安装

【Grok API 环境检测】(可选)
  ❌ xai-sdk: 未安装

============================================================
【环境检测总结】
============================================================

✅ 基础环境: 完整
   ✔️ 系统可以正常运行（仅文本提取功能）

⚠️  OCR 环境: 未完整安装
   ⚠️  无法识别扫描版 PDF（仅能处理文本型 PDF）

   安装方法:
   1. pip install pdf2image pytesseract
   2. brew install tesseract tesseract-lang poppler  (macOS)
```

根据检测结果决定是否需要安装额外功能。

---

## 📋 依赖文件说明

### requirements-minimal.txt（必需）
- Flask, pdfplumber, PyMuPDF, Pillow
- **功能**：文本型 PDF 识别
- **大小**：~10MB
- **安装时间**：5-10秒

### requirements-ocr.txt（推荐）
- pdf2image, pytesseract
- **功能**：扫描版 PDF 识别
- **大小**：~5MB
- **安装时间**：3-5秒
- **额外要求**：需安装 Tesseract（系统级）

### requirements-grok.txt（可选）
- xai-sdk
- **功能**：AI 智能识别
- **大小**：~2MB
- **安装时间**：3-5秒
- **额外要求**：需要 API Key（付费）

---

## 🎯 不同场景的推荐配置

### 场景1：只处理文字简历（大多数情况）
```bash
pip3 install -r requirements-minimal.txt
```
- ✅ 启动快
- ✅ 依赖少
- ✅ 完全免费
- ⚠️ 不支持扫描版

### 场景2：处理扫描版简历（推荐）
```bash
pip3 install -r requirements-minimal.txt
pip3 install -r requirements-ocr.txt
brew install tesseract tesseract-lang poppler
```
- ✅ 支持扫描版
- ✅ 准确率高
- ✅ 完全免费
- ⚠️ 需要额外安装

### 场景3：处理复杂格式（土豪版）
```bash
pip3 install -r requirements.txt
brew install tesseract tesseract-lang poppler
# + Grok API Key
```
- ✅ 最强识别
- ✅ 处理各种格式
- ⚠️ 需要付费 API

---

## 🚀 一键启动脚本（可选）

创建 `start.sh`（macOS/Linux）：

```bash
#!/bin/bash
echo "🔍 检查环境..."
python3 check_environment.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 环境检查通过，启动系统..."
    python3 app.py
else
    echo ""
    echo "❌ 环境检查失败，请安装依赖："
    echo "   pip3 install -r requirements-minimal.txt"
fi
```

使用：
```bash
chmod +x start.sh
./start.sh
```

---

## 📞 技术支持

### 常见问题

**Q: 用户说"不能识别扫描版PDF"？**
```bash
# 让用户运行环境检测
python3 check_environment.py

# 如果 OCR 显示 ❌，安装 OCR 环境
pip3 install -r requirements-ocr.txt
brew install tesseract tesseract-lang poppler
```

**Q: 用户说"pip 命令不存在"？**
```bash
# macOS/Linux 使用 pip3
pip3 install -r requirements-minimal.txt

# 或者使用 python -m pip
python3 -m pip install -r requirements-minimal.txt
```

**Q: 用户说"端口被占用"？**
```bash
# 修改 app.py 最后一行的端口号
app.run(host='0.0.0.0', port=5002, debug=True)  # 改成 5002
```

---

## 🎁 打包建议

### 最小打包（适合快速分享）
```
- 所有 .py 文件
- templates/ 文件夹
- requirements-minimal.txt
- README.md
- check_environment.py ⭐
```

### 完整打包（适合正式部署）
```
- 所有文件（包括文档）
- 不包括：
  - resumes.db（数据库会自动创建）
  - __pycache__/
  - .DS_Store
  - server.log
  - *.pyc
```

### 压缩命令

```bash
# 创建压缩包（排除不必要文件）
zip -r resume_system.zip . -x "*.pyc" "*.db" "__pycache__/*" ".DS_Store" "server.log" "pdf\ test/*"
```

---

## ✨ 总结

- ✅ **核心功能不依赖 OCR**，分享给别人完全没问题
- ✅ **自动降级设计**，缺少功能时会友好提示，不会崩溃
- ✅ **环境检测脚本**，让用户一目了然知道自己的环境状态
- ✅ **分层依赖**，用户可以按需安装，不强制全部安装
- ✅ **详细文档**，用户可以自助解决大部分问题

**推荐给别人时只需要说**：
1. "先运行 `python3 check_environment.py` 看看环境"
2. "至少安装 `pip3 install -r requirements-minimal.txt`"
3. "然后 `python3 app.py` 就能用了"

如果遇到问题，再根据环境检测结果进行针对性安装。

