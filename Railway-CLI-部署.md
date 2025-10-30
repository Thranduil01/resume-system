# 🚂 Railway CLI 直接部署（推荐）

## 🎯 不需要 GitHub，直接部署到 Railway！

这是**最简单**的部署方式，跳过 GitHub 步骤。

---

## 📦 步骤

### 1. 安装 Railway CLI

```bash
# macOS/Linux（使用 Homebrew）
brew install railway

# 或者使用 npm
npm install -g @railway/cli
```

### 2. 登录 Railway

```bash
railway login
```

**会自动打开浏览器，点击授权即可。**

---

### 3. 初始化项目

```bash
cd "/Users/zhanghan5/Downloads/6. coding/1030 intern_email_address"

# 初始化 Railway 项目
railway init
```

**选择**：
- 创建新项目（Create new project）
- 输入项目名称（如：resume-system）

---

### 4. 部署

```bash
# 部署到 Railway
railway up
```

**会自动**：
1. ✅ 上传代码
2. ✅ 检测为 Python 项目
3. ✅ 安装依赖
4. ✅ 启动应用
5. ✅ 生成访问 URL

---

### 5. 获取 URL

```bash
# 生成公开域名
railway domain
```

或者访问 Railway 网页端：
1. 打开 https://railway.app
2. 进入你的项目
3. Settings → Generate Domain
4. 复制 URL

---

## ✅ 完整命令（一次性执行）

```bash
# 1. 进入项目目录
cd "/Users/zhanghan5/Downloads/6. coding/1030 intern_email_address"

# 2. 安装 Railway CLI（如果还没有）
npm install -g @railway/cli

# 3. 登录
railway login

# 4. 初始化项目
railway init

# 5. 部署
railway up

# 6. 生成域名
railway domain
```

---

## 🎉 优势

| 方式 | 优势 | 缺点 |
|------|------|------|
| **Railway CLI** | ⚡ 最快<br>🔧 最简单<br>❌ 不需要 GitHub | 需要安装 CLI |
| **GitHub 部署** | 📚 代码托管<br>🔄 自动更新 | 需要配置认证 |

---

## 🔄 更新部署

修改代码后，重新部署：

```bash
railway up
```

**就这么简单！**

---

## 📊 查看日志

```bash
# 实时查看日志
railway logs

# 或在网页端查看
railway open
```

---

## 💡 常用命令

```bash
railway login      # 登录
railway init       # 初始化项目
railway up         # 部署
railway logs       # 查看日志
railway domain     # 生成/查看域名
railway open       # 在浏览器打开项目
railway status     # 查看项目状态
railway variables  # 管理环境变量
```

---

## ⚠️ 注意事项

### 1. 首次运行可能较慢
- 需要安装依赖（pip install）
- 需要构建环境
- 大约需要 3-5 分钟

### 2. OCR 功能
- 标准部署不支持 Tesseract OCR
- 推荐使用 Grok API 代替
- 或使用 Docker 部署

### 3. 环境变量
如果需要设置 Grok API Key：

```bash
railway variables set GROK_API_KEY="your-api-key"
```

---

## 🚀 快速开始

```bash
# 一键部署（复制粘贴运行）
cd "/Users/zhanghan5/Downloads/6. coding/1030 intern_email_address" && \
npm install -g @railway/cli && \
railway login && \
railway init && \
railway up && \
railway domain && \
echo "🎉 部署完成！"
```

---

## 📚 相关资源

- Railway CLI 文档：https://docs.railway.app/develop/cli
- Railway 官网：https://railway.app
- 项目仪表板：运行 `railway open`

---

**推荐使用这种方式，最简单快速！** 🚀

