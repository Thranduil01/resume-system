# 🚂 Railway 部署指南

## 📋 简介

Railway 是一个现代化的云部署平台，可以让你轻松将简历信息提取系统部署为在线服务。

**部署后的优势**：
- ✅ 任何人都可以通过 URL 访问
- ✅ 支持文件上传（无需本地路径）
- ✅ 自动 HTTPS 加密
- ✅ 免费额度（每月 5 美元额度）

---

## 🚀 快速部署步骤

### 1. 准备工作

**注册 Railway 账号**：
- 访问：https://railway.app
- 使用 GitHub 账号登录（推荐）

**安装 Git**（如果还没有）：
```bash
# macOS
brew install git

# Windows
# 从 https://git-scm.com/download/win 下载安装
```

---

### 2. 初始化 Git 仓库

打开终端，进入项目目录：

```bash
# 进入项目目录
cd "/path/to/1030 intern_email_address"

# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit"
```

---

### 3. 推送到 GitHub

**创建 GitHub 仓库**：
1. 访问 https://github.com
2. 点击右上角的 "+" → "New repository"
3. 输入仓库名（如 `resume-system`）
4. **不要**勾选 "Initialize this repository with a README"
5. 点击 "Create repository"

**推送代码**：
```bash
# 关联远程仓库（替换为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/resume-system.git

# 推送代码
git branch -M main
git push -u origin main
```

---

### 4. 在 Railway 部署

#### 方式1：从 GitHub 部署（推荐）⭐⭐⭐⭐⭐

1. **登录 Railway**：https://railway.app
2. **点击 "New Project"**
3. **选择 "Deploy from GitHub repo"**
4. **授权 GitHub**（如果第一次使用）
5. **选择你刚创建的仓库**（如 `resume-system`）
6. **等待自动部署**（约 2-5 分钟）

#### 方式2：使用 Railway CLI

```bash
# 安装 Railway CLI
npm install -g @railway/cli

# 登录
railway login

# 初始化项目
railway init

# 部署
railway up
```

---

### 5. 配置环境变量（可选）

如果需要设置默认的 Grok API Key 或其他配置：

1. 在 Railway 项目页面，点击 **"Variables"**
2. 添加环境变量：
   ```
   PORT=5001
   ```

---

### 6. 获取访问链接

部署完成后：
1. 在 Railway 项目页面，点击 **"Settings"**
2. 找到 **"Domains"** 部分
3. 点击 **"Generate Domain"**
4. 复制生成的 URL（如：`https://your-app.up.railway.app`）

**🎉 完成！** 现在任何人都可以通过这个 URL 访问你的系统。

---

## 📊 Railway 免费额度

| 项目 | 免费额度 |
|------|---------|
| 每月费用 | $5 USD（免费） |
| CPU | 共享 |
| 内存 | 512 MB |
| 存储 | 临时存储（重启后清空） |
| 流量 | 100 GB/月 |

**注意**：
- 上传的 PDF 文件在应用重启后会被清空（系统会自动删除临时文件）
- 数据库文件 `resumes.db` 会持久化保存
- 如果超出免费额度，需要升级到付费计划

---

## 🔧 项目配置文件说明

### `Procfile`
```
web: python app.py
```
告诉 Railway 如何启动应用。

### `requirements-minimal.txt`
列出了运行所需的 Python 包。

### `runtime.txt`（可选）
```
python-3.12.0
```
指定 Python 版本（如果需要）。

---

## ⚠️ 注意事项

### 1. 文件上传限制

在云端部署时，用户只能使用 **"☁️ 文件上传"** 模式，无法使用 **"📁 本地路径"** 模式。

**原因**：
- 云服务器无法访问用户的本地电脑文件系统
- 这是正常的，所有云服务都是这样

**解决方案**：
- 使用文件上传功能
- 系统会自动处理并删除临时文件

---

### 2. OCR 依赖

Railway 部署时，**Tesseract OCR 可能无法使用**（需要系统级依赖）。

**建议**：
- 使用 **Grok API** 进行智能识别
- 或者准备可提取文本的 PDF（非扫描版）

如果一定要使用 OCR，可以使用 Docker 部署（更复杂）。

---

### 3. 数据持久化

**持久化的数据**：
- ✅ 数据库文件（`resumes.db`）

**不持久化的数据**：
- ❌ 上传的临时 PDF 文件（处理后自动删除）
- ❌ 日志文件

---

## 🔄 更新部署

当你修改代码后，重新部署：

### 从 GitHub 部署
```bash
# 提交更改
git add .
git commit -m "Update features"
git push

# Railway 会自动检测并重新部署
```

### 使用 Railway CLI
```bash
railway up
```

---

## 🐛 常见问题

### Q: 部署失败？
**A**: 检查：
1. `requirements-minimal.txt` 是否完整
2. `Procfile` 是否正确
3. Railway 日志（点击 "Deployments" 查看）

### Q: 访问 URL 报错 502？
**A**: 
1. 检查 `app.py` 中的 `port` 配置：
   ```python
   port = int(os.environ.get('PORT', 5001))
   app.run(debug=True, host='0.0.0.0', port=port)
   ```
2. 等待部署完成（可能需要几分钟）

### Q: 数据丢失了？
**A**: 
- 如果是数据库数据，应该不会丢失
- 如果是上传的 PDF，这是正常的（临时文件）
- 检查 Railway 是否重启了实例

### Q: 想要自定义域名？
**A**: 
1. 在 Railway 项目设置中
2. 点击 "Custom Domain"
3. 输入你的域名并配置 DNS

---

## 💰 费用说明

### 免费额度
- 每月 $5 USD 的使用额度
- 对于小规模使用完全足够

### 超出免费额度
- 按实际使用量计费
- 可以在 Railway 仪表板查看当前使用量
- 可以设置预算提醒

### 如何节省费用
1. 不用时暂停项目（点击 "Settings" → "Pause"）
2. 优化代码，减少 CPU 和内存使用
3. 定期清理数据库

---

## 📚 相关资源

- Railway 官方文档：https://docs.railway.app
- Python 部署指南：https://docs.railway.app/deploy/deployments
- 常见问题：https://docs.railway.app/help/faq

---

## 🎯 部署检查清单

部署前确认：
- ✅ 所有依赖都在 `requirements-minimal.txt` 中
- ✅ `Procfile` 文件存在且正确
- ✅ `.gitignore` 配置正确（不提交 `.db` 文件、`uploads/` 等）
- ✅ 代码中使用了动态端口配置
- ✅ 测试过本地运行无误

部署后确认：
- ✅ Railway 显示部署成功（绿色）
- ✅ 访问 URL 能打开网页
- ✅ 文件上传功能正常
- ✅ 数据解析和存储正常
- ✅ 查看日志无严重错误

---

## 🚀 高级：Docker 部署（支持 OCR）

如果需要完整的 OCR 支持，可以使用 Docker：

### 1. 创建 `Dockerfile`
```dockerfile
FROM python:3.12-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \\
    tesseract-ocr \\
    tesseract-ocr-chi-sim \\
    poppler-utils \\
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements-minimal.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements-minimal.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 5001

# 启动命令
CMD ["python", "app.py"]
```

### 2. 在 Railway 部署
- Railway 会自动检测 Dockerfile 并使用 Docker 部署
- 这样就能完整支持 OCR 功能了

---

**祝部署顺利！** 🎉

如有问题，请查看 Railway 日志或联系技术支持。

