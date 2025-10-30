# 🔧 Render 部署问题排查指南

## ✅ 已修复的问题

已经修复了 `app.py` 中的 debug 设置问题，代码已推送到 GitHub。

**修复内容**：
- ✅ 生产环境自动关闭 debug 模式
- ✅ 本地开发保留 debug 模式

---

## 📋 详细部署步骤（跟我一步步来）

### 步骤1：确认 GitHub 代码最新

**在 Render 部署前，先确认代码已更新！**

1. 访问你的 GitHub 仓库：https://github.com/Thranduil01/resume-system
2. 检查最后一次提交是否是：`Fix: Set debug=False for production environment`
3. 如果不是，等待几秒钟刷新页面

---

### 步骤2：登录 Render

1. **访问** https://render.com
2. **点击右上角** `Sign In`
3. **选择** `Sign in with GitHub`（推荐）
4. **授权** Render 访问你的 GitHub 账号

---

### 步骤3：创建 Web Service

1. **点击** `New +`（右上角蓝色按钮）
2. **选择** `Web Service`

---

### 步骤4：连接 GitHub 仓库

#### 如果是第一次使用 Render

1. **点击** `Connect account`（连接 GitHub）
2. **选择** `All repositories`（所有仓库）或 `Only select repositories`（选择特定仓库）
3. **点击** `Install`

#### 如果已经连接过

1. 在仓库列表中找到 `resume-system`
2. **点击** 右侧的 `Connect` 按钮

---

### 步骤5：配置 Web Service（重要！）

填写以下配置（**一字不差**）：

```
┌─────────────────────────────────────────┐
│ Name                                     │
│ resume-system                            │ ← 可以改成你喜欢的名字
├─────────────────────────────────────────┤
│ Region                                   │
│ Oregon (US West)                         │ ← 或选择离你最近的
├─────────────────────────────────────────┤
│ Branch                                   │
│ main                                     │ ← 必须是 main
├─────────────────────────────────────────┤
│ Root Directory                           │
│ （留空）                                  │
├─────────────────────────────────────────┤
│ Runtime                                  │
│ Python 3                                 │ ← 自动检测，不用改
├─────────────────────────────────────────┤
│ Build Command                            │
│ pip install -r requirements-minimal.txt  │ ← 复制粘贴
├─────────────────────────────────────────┤
│ Start Command                            │
│ python app.py                            │ ← 复制粘贴
└─────────────────────────────────────────┘
```

**⚠️ 重要提示**：
- **Build Command** 使用 `requirements-minimal.txt`（不是 `requirements.txt`）
- **Start Command** 是 `python app.py`（不是 `gunicorn`）

---

### 步骤6：选择计划

1. **向下滚动**，找到 `Instance Type`
2. **选择** `Free`（免费计划）
3. **点击** `Create Web Service`（底部蓝色按钮）

---

### 步骤7：等待部署

部署过程会显示实时日志：

```
==> Cloning from https://github.com/Thranduil01/resume-system...
==> Checking out commit 5d555dd...
==> Installing dependencies...
==> Building...
==> Starting service...
```

**正常情况**：
- ⏳ 第一次部署需要 **3-5 分钟**
- ✅ 看到 `Your service is live 🎉` 就成功了

---

## 🔍 常见问题排查

### 问题1：Build 失败

**错误信息**：
```
ERROR: Could not find a version that satisfies the requirement...
```

**解决方案**：
1. 检查 Build Command 是否正确：
   ```
   pip install -r requirements-minimal.txt
   ```
2. 确认 GitHub 仓库中有 `requirements-minimal.txt` 文件

---

### 问题2：Start 失败

**错误信息**：
```
Application failed to respond
```

**可能原因**：
1. Start Command 不正确
2. 端口配置问题
3. 代码有错误

**解决方案**：

#### A. 检查 Start Command
应该是：
```
python app.py
```

**不是**：
- ❌ `gunicorn app:app`
- ❌ `flask run`
- ❌ `python3 app.py`（Render 用 `python` 不是 `python3`）

#### B. 查看日志
1. 在 Render 项目页面，点击 `Logs`（左侧菜单）
2. 查看错误信息
3. 截图发给我，我帮你分析

---

### 问题3：部署成功但打不开

**症状**：
- Render 显示 `Live`（绿色）
- 但访问 URL 显示错误或空白

**解决方案**：

#### A. 等待唤醒（如果是第一次访问）
免费计划有休眠机制：
- 15 分钟无活动会休眠
- 首次访问需要 30-50 秒唤醒
- **刷新页面等待**

#### B. 检查 URL
确保访问的是 Render 生成的 URL：
```
https://your-app-name.onrender.com
```

**不是**：
- ❌ `http://localhost:5001`
- ❌ `http://127.0.0.1:5001`

---

### 问题4：一直在 "Building"

**症状**：
- 卡在 "In Progress" 状态超过 10 分钟

**解决方案**：
1. **取消部署**：点击 `Cancel Deploy`
2. **手动重新部署**：点击 `Manual Deploy` → `Deploy latest commit`
3. **检查依赖**：确认 `requirements-minimal.txt` 文件正确

---

## 🔍 如何查看日志

### 实时日志
1. 进入你的 Render 项目页面
2. 点击左侧 `Logs`
3. 查看实时输出

### 查找错误
日志中常见的关键词：
- ❌ `ERROR`：错误
- ❌ `FAILED`：失败
- ❌ `ModuleNotFoundError`：缺少依赖
- ✅ `Your service is live`：成功

---

## 📝 正确的配置总结

### Render 配置（复制粘贴）

```yaml
Name: resume-system
Region: Oregon (US West)
Branch: main
Root Directory: （留空）
Runtime: Python 3
Build Command: pip install -r requirements-minimal.txt
Start Command: python app.py
Instance Type: Free
```

### 文件清单（GitHub 仓库应该有这些）

```
✅ app.py                           # 主应用
✅ database.py                      # 数据库
✅ pdf_parser.py                    # PDF 解析
✅ pdf_parser_enhanced.py           # 增强解析
✅ requirements-minimal.txt         # 依赖列表
✅ Procfile                         # 部署配置
✅ templates/index.html             # 前端页面
✅ .gitignore                       # Git 忽略
```

---

## 🎯 完整部署流程图

```
开始
  ↓
确认 GitHub 代码最新
  ↓
登录 Render (使用 GitHub)
  ↓
New + → Web Service
  ↓
选择 resume-system 仓库
  ↓
配置 (Build Command, Start Command)
  ↓
选择 Free 计划
  ↓
Create Web Service
  ↓
等待 3-5 分钟
  ↓
部署成功！
  ↓
复制 URL
  ↓
访问测试（首次可能需要等 30 秒唤醒）
  ↓
完成！
```

---

## 🆘 如果还是不行

**请告诉我以下信息**：

1. **当前状态**：
   - [ ] Build 阶段失败
   - [ ] Start 阶段失败
   - [ ] 部署成功但打不开
   - [ ] 其他：___________

2. **错误信息**：
   - 截图 Render 的日志页面
   - 或复制粘贴错误信息

3. **配置信息**：
   - Build Command 是什么：___________
   - Start Command 是什么：___________

---

## 📞 获取帮助

### 查看 Render 日志
```
项目页面 → Logs → 查看实时日志
```

### 查看 Render 设置
```
项目页面 → Settings → 检查配置
```

### 手动重新部署
```
项目页面 → Manual Deploy → Deploy latest commit
```

---

## 🎉 部署成功的标志

### 在 Render 看到
```
✅ Live（绿色状态）
✅ Your service is live 🎉
✅ 有一个 URL 显示（如：https://resume-system-xxx.onrender.com）
```

### 访问 URL 看到
```
✅ 简历信息提取系统页面
✅ 有 "📁 本地路径" 和 "☁️ 文件上传" 两个选项
✅ 页面样式正常显示
```

---

## 💡 温馨提示

1. **首次访问慢**是正常的（休眠唤醒需要 30-50 秒）
2. **使用 "☁️ 文件上传" 模式**（云端不支持本地路径）
3. **数据会持久化保存**（不会丢失）
4. **可以分享 URL** 给任何人使用

---

**现在告诉我你遇到的具体问题，我来帮你解决！** 🚀

