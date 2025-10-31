# Render 部署指南 - 线上版

## 🚀 方案一：指定根目录部署（推荐）

在 Render 创建 Web Service 时，指定 `online` 文件夹为根目录。

### 步骤：

1. **登录 Render**：https://dashboard.render.com

2. **创建 New Web Service**

3. **连接 GitHub 仓库**：
   - 选择 `Thranduil01/resume-system`

4. **配置部署设置**：
   ```
   Name:           resume-system
   Region:         Singapore (或其他)
   Branch:         main
   Root Directory: online          ⬅️ 关键：指定 online 文件夹
   Runtime:        Python 3
   Build Command:  pip install -r requirements-compatible.txt
   Start Command:  gunicorn --bind 0.0.0.0:$PORT app:app
   ```
   
   > 💡 **说明**：使用 Gunicorn 作为生产服务器，而不是 Flask 开发服务器

5. **选择套餐**：
   - Free（免费，但会休眠）
   - 或付费套餐（$7/月起）

6. **点击 "Create Web Service"**

7. **等待部署完成**（大约 3-5 分钟）

8. **访问您的应用**：
   - Render 会提供一个类似 `https://resume-system.onrender.com` 的地址

---

## 🔧 方案二：使用 render.yaml 自动部署

如果使用 Blueprint（自动部署），Render 会读取 `online/render.yaml` 配置。

### 步骤：

1. **在 Render Dashboard 选择 "Blueprints"**

2. **连接 GitHub 仓库**

3. **Render 会自动检测到 `online/render.yaml`**

4. **确认配置并部署**

---

## ⚙️ 环境变量（可选）

如果需要配置环境变量（如 Grok API Key），在 Render Dashboard 中：

1. 进入 Web Service
2. 点击 "Environment"
3. 添加环境变量：
   ```
   GROK_API_KEY=your_api_key_here
   ```

然后修改 `app.py` 读取环境变量：
```python
import os
grok_api_key = os.environ.get('GROK_API_KEY')
```

---

## 📝 注意事项

### 1. 数据持久化
⚠️ **重要**：Render 的免费套餐文件系统不持久化，重启后数据库会丢失。

**解决方案**：
- 升级到付费套餐（包含持久磁盘）
- 或使用外部数据库（如 PostgreSQL）

### 2. 休眠问题
免费套餐会在 15 分钟无活动后休眠，下次访问需要等待 30 秒唤醒。

**解决方案**：
- 升级到付费套餐
- 使用定时 ping 服务（如 UptimeRobot）

### 3. 文件上传限制
Render 有请求大小限制（通常 100MB）。

当前配置：单个 PDF 最大 50MB（已在代码中设置）

---

## 🔍 部署后检查清单

✅ 网站能正常访问  
✅ 文件上传功能正常  
✅ 可以解析 PDF 并提取信息  
✅ 数据展示正常  
✅ 确认**没有**本地路径输入框（线上版特征）  

---

## 🐛 常见问题

### Q1: 部署失败 - "No such file or directory"
**原因**：可能没有正确设置 Root Directory  
**解决**：在 Render 设置中确认 Root Directory 设置为 `online`

### Q2: 应用运行但无法访问
**原因**：端口配置问题  
**解决**：确认 `app.py` 使用 `PORT` 环境变量（已配置）

### Q3: PDF 解析失败
**原因**：可能缺少系统依赖  
**解决**：检查 Render 日志，确认 PyMuPDF 正确安装

### Q4: 数据库数据丢失
**原因**：免费套餐不持久化文件  
**解决**：升级到付费套餐或使用外部数据库

---

## 📊 对比：本地版 vs 线上版

| 项目 | 本地版（根目录） | 线上版（online/） |
|------|-----------------|------------------|
| 本地路径输入 | ✅ 有 | ❌ 无（安全） |
| 文件上传 | ✅ 有 | ✅ 有 |
| 适合场景 | 个人电脑 | ✅ Render 部署 |
| 安全性 | 本地安全 | ✅ 更安全 |

---

## 🔗 相关链接

- **Render 文档**：https://render.com/docs
- **GitHub 仓库**：https://github.com/Thranduil01/resume-system
- **Python 部署指南**：https://render.com/docs/deploy-flask

---

## 💡 推荐配置

**开发环境**：使用根目录的本地版  
**生产环境**：部署 `online/` 文件夹到 Render  

这样既保留了本地使用的便利性，又保证了线上部署的安全性！

---

**最后更新**：2025年10月  
**版本**：线上部署版 1.0

