# 🚀 Render.com 免费部署指南

## 🎯 优势

- ✅ **完全免费**（无需信用卡）
- ✅ 自动 HTTPS
- ✅ 简单易用
- ✅ 从 GitHub 自动部署
- ✅ 免费额度：750 小时/月

---

## 📋 部署步骤

### 步骤1：推送代码到 GitHub

#### 方法1：删除旧仓库，重新创建

1. **删除有问题的仓库**：
   - 访问：https://github.com/Thranduil01/resume-system/settings
   - 滚动到底部 → `Danger Zone` → `Delete this repository`
   - 输入仓库名确认删除

2. **创建新仓库**：
   - 访问：https://github.com/new
   - 仓库名：`resume-system`
   - **不要勾选**任何初始化选项（README、.gitignore 等）
   - 点击 `Create repository`

3. **推送代码**：
   ```bash
   cd "/Users/zhanghan5/Downloads/6. coding/1030 intern_email_address"
   
   # 更新远程地址
   git remote set-url origin https://github.com/Thranduil01/resume-system.git
   
   # 推送
   git push -u origin main
   ```

#### 方法2：使用 SSH（如果配置了）

```bash
cd "/Users/zhanghan5/Downloads/6. coding/1030 intern_email_address"

# 切换到 SSH
git remote set-url origin git@github.com:Thranduil01/resume-system.git

# 推送
git push -u origin main
```

---

### 步骤2：在 Render 部署

1. **访问 Render**：https://render.com

2. **注册/登录**：
   - 使用 GitHub 账号登录（推荐）
   - 或使用邮箱注册

3. **创建 Web Service**：
   - 点击 `New +` → `Web Service`
   - 选择 `Connect account`（连接 GitHub）
   - 授权 Render 访问你的仓库
   - 选择 `resume-system` 仓库

4. **配置服务**：
   ```
   Name: resume-system
   Region: Oregon (US West) 或离你最近的
   Branch: main
   Runtime: Python 3
   Build Command: pip install -r requirements-minimal.txt
   Start Command: python app.py
   ```

5. **选择计划**：
   - 选择 `Free`（免费计划）

6. **创建服务**：
   - 点击 `Create Web Service`
   - 等待部署（约 3-5 分钟）

---

### 步骤3：配置环境变量（可选）

如果需要设置 Grok API Key：

1. 在 Render 项目页面，点击 `Environment`
2. 添加环境变量：
   ```
   Key: GROK_API_KEY
   Value: your-api-key
   ```
3. 点击 `Save Changes`

---

### 步骤4：获取 URL

部署成功后：
- Render 会自动生成一个 URL
- 格式：`https://your-app-name.onrender.com`
- 复制这个 URL 分享给团队

---

## 🔧 重要配置

### 需要修改 `app.py` 的端口配置

Render 使用环境变量 `PORT`，确保 `app.py` 支持：

```python
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    
    print("=" * 50)
    print("简历信息提取系统已启动")
    print(f"请在浏览器中访问: http://127.0.0.1:{port}")
    print("=" * 50)
    app.run(debug=False, host='0.0.0.0', port=port)  # 注意：debug=False
```

**✅ 你的 `app.py` 已经正确配置了！**

---

## 📊 免费计划限制

| 项目 | 限制 |
|------|------|
| 实例数 | 1 个 |
| 内存 | 512 MB |
| CPU | 共享 |
| 带宽 | 100 GB/月 |
| 运行时间 | 750 小时/月 |
| 休眠 | 15 分钟无活动后休眠 |

**注意**：
- 应用会在 15 分钟无活动后自动休眠
- 下次访问时会自动唤醒（可能需要 30 秒）
- 这是免费计划的正常行为

---

## 🔄 自动部署

配置完成后：
1. 你推送到 GitHub 的任何更改
2. Render 会**自动检测**并重新部署
3. 无需手动操作

---

## ⚠️ 注意事项

### 1. OCR 功能
- Render 免费计划**不支持** Tesseract OCR
- 推荐使用 **Grok API** 代替

### 2. 文件上传
- 使用 "☁️ 文件上传" 模式
- 不能使用 "📁 本地路径" 模式

### 3. 数据持久化
- 数据库文件会持久化
- 但应用重启后 `uploads/` 文件夹会清空（这是正常的）

### 4. 休眠机制
- 15 分钟无活动会休眠
- 下次访问自动唤醒（约 30 秒）
- 如需保持常开，考虑付费计划或定时 ping

---

## 🆚 Render vs Railway

| 特性 | Render | Railway |
|------|--------|---------|
| **免费额度** | 750小时/月 | $5/月 |
| **信用卡** | ❌ 不需要 | ⚠️ 可能需要 |
| **休眠** | 15分钟后休眠 | 不休眠 |
| **部署方式** | GitHub | GitHub/CLI |
| **适合新手** | ✅ | ✅ |

---

## 🚀 快速开始

### 完整命令（复制粘贴）

```bash
# 1. 进入项目目录
cd "/Users/zhanghan5/Downloads/6. coding/1030 intern_email_address"

# 2. 删除旧的远程仓库配置
git remote remove origin

# 3. 在 GitHub 创建新仓库（在浏览器操作）
# 访问：https://github.com/new
# 仓库名：resume-system
# 不勾选任何初始化选项

# 4. 添加新的远程仓库
git remote add origin https://github.com/Thranduil01/resume-system.git

# 5. 推送代码
git push -u origin main

# 6. 在 Render 部署（在浏览器操作）
# 访问：https://render.com
# 按照上面的步骤操作
```

---

## 💡 其他免费替代方案

如果 Render 也不满意，还有这些选择：

### 1. Fly.io
- 免费额度：3 个小型应用
- 不需要信用卡
- 支持 Dockerfile
- https://fly.io

### 2. Vercel
- 免费且无限制
- 但主要针对前端应用
- Python 支持有限
- https://vercel.com

### 3. Heroku（需要信用卡）
- 经典的部署平台
- 免费计划已取消
- 需要付费（$5-7/月）
- https://heroku.com

---

## 📚 相关资源

- Render 官方文档：https://render.com/docs
- Render Python 指南：https://render.com/docs/deploy-flask
- GitHub 仓库设置：https://github.com/Thranduil01/resume-system/settings

---

## 🎉 总结

**推荐使用 Render！**

优势：
- ✅ 完全免费
- ✅ 不需要信用卡
- ✅ 自动从 GitHub 部署
- ✅ 自动 HTTPS
- ✅ 750 小时免费额度

唯一缺点：
- ⚠️ 15 分钟无活动会休眠（下次访问自动唤醒）

**对于个人项目或演示，这完全够用！** 🚀

