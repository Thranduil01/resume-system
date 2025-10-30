# 📄 简历信息提取系统

一个基于 Web 的 PDF 简历信息自动提取工具，可以从 PDF 简历中自动提取邮箱、学校、年级等关键信息，并存储到数据库中。

## ✨ 功能特点

- 🎯 **三级智能识别**：文本提取 → OCR 识别 → Grok AI 识别（自动降级）
- 🤖 **AI 驱动**：支持 Grok API 智能识别，处理扫描版和复杂布局简历
- 🔍 **OCR 支持**：自动识别扫描版 PDF，提取文字信息
- 💾 **数据库存储**：使用 SQLite 数据库持久化存储所有提取的信息
- 🌐 **现代化 Web 界面**：美观、易用的网页操作界面
- 📋 **一键复制**：支持一键复制所有邮箱（分号分隔）
- 📊 **Markdown 表格**：自动生成 Markdown 格式的数据表格，方便分享
- 🔄 **批量处理**：支持批量解析整个文件夹的 PDF 文件
- 📈 **实时统计**：显示简历总数和邮箱数量统计，识别方式统计

## 🛠️ 技术栈

- **后端**：Flask (Python Web 框架)
- **前端**：HTML + CSS + JavaScript (原生)
- **PDF 解析**：pdfplumber
- **数据库**：SQLite
- **正则表达式**：用于信息提取

## 📦 安装步骤

### 🔍 环境检测（推荐先运行）

```bash
cd "/Users/zhanghan5/Downloads/6. coding/1030 intern_email_address"
python3 check_environment.py
```

这会检测您的系统环境，告诉您哪些功能可用。

---

### 方案1：最小安装（仅文本型 PDF）⚡

```bash
pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements-minimal.txt
```

**适用场景**：
- ✅ 只处理正常的文本型 PDF
- ✅ 不需要 OCR 功能
- ✅ 快速安装，无需额外软件

---

### 方案2：推荐安装（支持扫描版 PDF）⭐ 推荐

```bash
# 1. 安装基础依赖
pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements-minimal.txt

# 2. 安装 OCR 依赖
pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements-ocr.txt

# 3. 安装 Tesseract OCR（macOS）
brew install tesseract tesseract-lang poppler
```

**适用场景**：
- ✅ 处理扫描版 PDF
- ✅ 准确率高（70-90%）
- ✅ 完全免费

**详细安装指南**：查看 [INSTALL_OCR.md](INSTALL_OCR.md)

---

### 方案3：完整安装（AI 智能识别）🚀

```bash
# 1. 安装所有依赖
pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# 2. 安装 OCR 环境（同方案2）
brew install tesseract tesseract-lang poppler

# 3. 获取 Grok API Key
# 访问 https://x.ai 获取
```

**适用场景**：
- ✅ 最强大的识别能力
- ✅ 处理复杂布局
- ⚠️ 需要 API Key（付费）

**详细使用指南**：查看 [GROK_API_GUIDE.md](GROK_API_GUIDE.md)

## 🚀 使用方法

### 1. 启动服务器

```bash
python app.py
```

启动成功后，你会看到：

```
==================================================
简历信息提取系统已启动
请在浏览器中访问: http://127.0.0.1:5000
==================================================
```

### 2. 打开网页

在浏览器中访问：`http://127.0.0.1:5000`

### 3. 解析 PDF 简历

1. 在输入框中输入 PDF 文件夹的完整路径，例如：
   - `/Users/username/Documents/resumes`
   - `/Users/zhanghan5/Downloads/简历文件夹`

2. 点击 **"🚀 开始解析"** 按钮

3. 系统会自动解析文件夹中的所有 PDF 文件，提取信息并存入数据库

### 4. 查看结果

页面会自动显示：

- **统计卡片**：显示简历总数和邮箱数量
- **邮箱列表**：所有提取到的邮箱（去重），点击即可复制
- **数据表格**：完整的简历信息表格（HTML 格式）
- **Markdown 表格**：可一键复制的 Markdown 格式表格

### 5. 其他功能

- **🔄 刷新数据**：重新加载数据库中的数据
- **🗑️ 清空数据库**：删除所有已存储的记录
- **📋 复制邮箱**：点击邮箱区域，一键复制所有邮箱
- **📋 复制 Markdown**：一键复制 Markdown 格式的表格

## 📁 项目结构

```
1030 intern_email_address/
├── app.py                      # Flask 主应用
├── database.py                 # 数据库模型和操作
├── pdf_parser.py              # PDF 解析器
├── PDF_to_email_no_ocr.py     # 原始的邮箱提取脚本（命令行版）
├── requirements.txt           # 项目依赖
├── README.md                  # 说明文档
├── resumes.db                 # SQLite 数据库（运行后自动生成）
└── templates/
    └── index.html             # 前端页面
```

## 🎨 界面预览

系统提供了现代化、美观的用户界面，包含：

- 渐变色主题设计
- 响应式布局
- 实时状态提示
- 加载动画
- 交互式按钮和输入框

## 📝 提取的信息字段

| 字段 | 说明 |
|------|------|
| 文件名 | PDF 文件的名称 |
| 邮箱 | 从简历中提取的电子邮箱地址 |
| 本科学校 | 本科就读的学校名称 |
| 研究生学校 | 研究生就读的学校名称（如有） |
| 当前年级 | 当前年级信息（如：大三、研一等） |
| 创建时间 | 记录创建时间 |

## 🔍 三级智能识别策略

系统采用**三级智能识别**，自动选择最佳方案：

### 📝 第一级：文本提取（默认）
- 使用 pdfplumber 直接提取 PDF 文本
- **速度**：最快（< 1秒/文件）
- **成本**：免费
- **适用**：正常文本型 PDF（约 80% 的简历）

### 🔍 第二级：OCR 识别（可选）
- 当文本提取失败时，自动使用 Tesseract OCR
- **速度**：较慢（3-5秒/文件）
- **成本**：免费
- **适用**：扫描版 PDF、图片型简历
- **准确率**：70-90%

### 🤖 第三级：Grok AI 识别（可选）
- 当 OCR 也失败时，调用 Grok Vision API
- **速度**：快（1-2秒/文件）
- **成本**：付费（按 API 调用量）
- **适用**：所有类型的 PDF，尤其是复杂布局
- **准确率**：90-98%

### 提取的信息
- **邮箱**：正则表达式 + AI 语义理解
- **学校**：关键词匹配 + 上下文分析
- **年级**：多种格式识别（中文、英文、数字）

## 💪 容错性和兼容性

### ✅ 无 OCR 环境也能正常运行

系统设计为**渐进增强**模式：
- **基础功能**（文本提取）：始终可用，不需要任何额外软件
- **OCR 功能**：如果未安装，系统会自动跳过，不会报错
- **Grok API**：如果未安装 SDK 或未提供 Key，系统会自动跳过

**示例输出**（无 OCR 环境）：
```
⚠️ OCR 环境未安装，跳过 OCR 识别
   提示：如需使用 OCR，请安装：pip install pdf2image pytesseract
```

系统会继续运行，只是无法识别扫描版 PDF。

### 🔄 三级识别策略（自动降级）

```
第1级：文本提取 → 成功 ✅
    ↓ 失败
第2级：OCR 识别 → 成功 ✅（需要环境）
    ↓ 失败或未安装
第3级：Grok API → 成功 ✅（需要 API Key）
    ↓ 失败或未配置
结果：标记为"未提取到信息"⚠️
```

**发给别人使用**：
- 只安装 `requirements-minimal.txt` 即可运行
- 缺少 OCR 时会显示友好提示，不会崩溃
- 所有功能都是可选的，核心功能始终可用

---

## ⚠️ 注意事项

1. **最小要求**：只需要 Python 3.7+ 和基础依赖即可运行
2. **路径格式**：请使用完整的绝对路径，例如：`/Users/username/Documents/resumes`
3. **中文支持**：完全支持中文简历和中文路径
4. **数据安全**：所有数据存储在本地 SQLite 数据库中
5. **浏览器兼容性**：建议使用现代浏览器（Chrome、Firefox、Safari、Edge）
6. **OCR 可选**：如果不需要识别扫描版 PDF，可以不安装 OCR

## 🐛 常见问题

### Q1: 无法提取到邮箱/学校/年级？
**A**: 可能原因：
- PDF 是扫描版（纯图片），需要 OCR 支持
- 简历格式不规范，信息位置特殊
- 使用了特殊字体或编码

### Q2: 启动时提示端口被占用？
**A**: 可以在 `app.py` 中修改端口号：
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # 改为 5001 或其他端口
```

### Q3: 数据库文件在哪里？
**A**: 数据库文件 `resumes.db` 会在项目根目录自动创建。

## 🔧 扩展功能

如果需要更高级的功能，可以考虑：

1. **OCR 支持**：添加 OCR 功能支持扫描版 PDF
2. **导出功能**：导出为 Excel、CSV 等格式
3. **批量邮件**：直接通过系统发送邮件
4. **高级搜索**：按学校、年级筛选
5. **数据分析**：统计学校分布、年级分布等

## 📄 许可证

本项目仅供学习和个人使用。

## 👤 作者

Zhang Han

## 🙏 致谢

感谢以下开源项目：
- Flask - Web 框架
- pdfplumber - PDF 解析
- SQLite - 轻量级数据库

---

**祝使用愉快！如有问题，请及时反馈。** 🎉


