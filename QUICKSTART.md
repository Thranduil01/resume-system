# 🚀 快速开始指南

## ⚡ 3步启动（最快）

```bash
# 1. 检查环境（5秒）
python3 check_environment.py

# 2. 安装依赖（10秒）
pip3 install -r requirements-minimal.txt

# 3. 启动
python3 app.py
```

访问：http://127.0.0.1:5001

---

## 📋 功能对照表

| 功能 | 最小安装 | +OCR | +Grok |
|------|---------|------|-------|
| 文本型 PDF | ✅ | ✅ | ✅ |
| 扫描版 PDF | ❌ | ✅ | ✅ |
| 复杂布局 | ❌ | ⚠️ | ✅ |
| 安装时间 | 10秒 | 2分钟 | 2分钟 |
| 是否免费 | ✅ | ✅ | ❌ |

---

## 💡 推荐配置

### 给普通用户（70%的情况够用）

```bash
pip3 install -r requirements-minimal.txt
python3 app.py
```

- ✅ 够用：大部分简历都是文本型 PDF
- ✅ 快速：10秒安装完成
- ✅ 简单：无需额外配置

### 给高级用户（处理扫描版）

```bash
# Python 依赖
pip3 install -r requirements-minimal.txt
pip3 install -r requirements-ocr.txt

# 系统依赖（macOS）
brew install tesseract tesseract-lang poppler

# 启动
python3 app.py
```

- ✅ 强大：处理扫描版 PDF
- ✅ 免费：不需要 API
- ⚠️ 稍慢：需要 2 分钟安装

---

## 🎯 容错性说明

### ✅ 不会崩溃的情况

- ❌ 没装 OCR → ⚠️ 提示"跳过 OCR 识别"
- ❌ 没装 Grok SDK → ⚠️ 提示"跳过 Grok API"
- ❌ 某个 PDF 读不出来 → ⚠️ 显示"未提取到信息"
- ❌ 文件夹不存在 → ⚠️ 提示"路径不存在"

**结论**：所有错误都会友好提示，不会导致程序崩溃！

---

## 📞 常见问题（1分钟解决）

### Q1: `pip: command not found`

```bash
# 用 pip3 代替
pip3 install -r requirements-minimal.txt
```

### Q2: 端口被占用

```bash
# 杀掉占用进程
lsof -ti:5001 | xargs kill -9

# 或者修改端口（在 app.py 最后一行）
app.run(host='0.0.0.0', port=5002, debug=True)
```

### Q3: 识别不出扫描版 PDF

```bash
# 安装 OCR
pip3 install -r requirements-ocr.txt
brew install tesseract tesseract-lang poppler
```

### Q4: 想知道我的环境状态

```bash
python3 check_environment.py
```

---

## 🎁 一键启动（推荐）

```bash
# 赋予执行权限（只需一次）
chmod +x start.sh

# 以后每次启动
./start.sh
```

这个脚本会：
1. ✅ 自动检查环境
2. ✅ 自动停止旧进程
3. ✅ 启动新服务
4. ⚠️ 环境不完整时给出安装提示

---

## 📦 分享给别人

只需打包以下核心文件：

```
必需：
- *.py (所有Python文件)
- templates/index.html
- requirements-minimal.txt
- check_environment.py
- README.md

可选：
- requirements-ocr.txt
- requirements-grok.txt
- DEPLOYMENT.md（部署文档）
- start.sh（一键启动）
```

压缩命令：
```bash
zip -r resume_system.zip *.py templates/ requirements*.txt *.md *.sh -x "__pycache__/*" "*.pyc" "*.db"
```

对方只需：
```bash
unzip resume_system.zip
cd resume_system
python3 check_environment.py  # 检查环境
pip3 install -r requirements-minimal.txt  # 安装
python3 app.py  # 启动
```

---

## ✨ 核心优势

1. **容错性强** - 缺少功能不会崩溃
2. **渐进增强** - 按需安装，不强制全装
3. **自我检测** - 一键了解环境状态
4. **友好提示** - 错误时给出明确安装指南
5. **分层依赖** - 最小、OCR、Grok 三档可选

---

## 🎊 开始使用

```bash
# 最简单的方式
python3 check_environment.py && pip3 install -r requirements-minimal.txt && python3 app.py
```

**就这么简单！🚀**

