# 简历信息提取系统 - 线上部署版

这是专为线上部署准备的版本，仅保留**文件上传功能**，移除了本地路径输入功能，避免安全隐患和使用混淆。

## 📋 功能特点

✅ 仅支持文件上传模式（安全可靠）  
✅ 支持批量上传PDF文件  
✅ 三级智能识别（文本提取 → OCR → Grok AI）  
✅ 自动提取邮箱、姓名、学校、年级  
✅ 美观的数据展示和导出功能  

## 🚀 快速开始

### 1. 安装依赖

推荐使用兼容版本：
```bash
pip install -r requirements-compatible.txt
```

或使用最小依赖版本：
```bash
pip install -r requirements-minimal.txt
```

### 2. 启动服务

```bash
python app.py
```

默认访问地址：http://127.0.0.1:5001

### 3. 使用方法

1. 在浏览器中打开系统
2. 点击上传区域或拖拽PDF文件
3. 可选：在"高级选项"中配置 OCR 和 Grok API
4. 点击"开始解析"
5. 查看提取结果

## 🌐 部署到云平台

本系统支持部署到各种云平台（Heroku, Railway, Render 等）。

### 环境变量

系统会自动检测 `PORT` 环境变量，适配云平台的动态端口分配。

### 部署步骤示例（以 Railway 为例）

1. 将 `online` 文件夹内容推送到 Git 仓库
2. 在 Railway 创建新项目并连接仓库
3. Railway 会自动检测 Flask 应用并部署
4. 系统会在环境变量 `PORT` 指定的端口上运行

### Heroku 部署

需要额外创建 `Procfile`：
```
web: python app.py
```

## 📦 文件结构

```
online/
├── app.py                      # Flask 应用（仅文件上传）
├── database.py                 # 数据库操作
├── pdf_parser.py               # 基础PDF解析
├── pdf_parser_enhanced.py      # 增强版解析（OCR + Grok）
├── requirements-compatible.txt # 兼容版依赖
├── requirements-minimal.txt    # 最小依赖
├── templates/
│   └── index.html             # 前端页面（仅上传模式）
├── uploads/                   # 临时上传文件夹
└── README.md                  # 本文档
```

## 🔒 安全说明

此版本**不支持**本地路径输入功能，因为：
- ❌ 线上环境不应允许用户访问服务器文件系统
- ❌ 避免路径遍历等安全风险
- ❌ 防止用户混淆使用方式

如需本地路径功能，请使用根目录下的本地开发版本。

## ⚙️ 高级选项

### OCR 识别
- 当PDF为扫描版或文本提取失败时自动使用
- 基于 PyMuPDF 的光学字符识别

### Grok AI 智能识别
- 使用 xAI 的视觉模型智能识别简历
- 适用于复杂格式、图片简历
- 需要 API Key（从 https://x.ai 获取）

## 📊 数据管理

- 数据存储在 SQLite 数据库 `resumes.db`
- 上传的文件处理后自动删除
- 可随时清空数据库重新开始

## 🆚 本地版 vs 线上版

| 功能 | 本地版 | 线上版 |
|------|--------|--------|
| 文件上传 | ✅ | ✅ |
| 本地路径输入 | ✅ | ❌ |
| 适用场景 | 个人电脑使用 | 云端部署 |
| 安全性 | 本地使用安全 | 移除路径功能更安全 |

## 📝 注意事项

1. 上传文件大小限制：单个文件最大 50MB
2. 上传的文件处理后会自动删除，不会占用服务器空间
3. 建议启用 OCR 以提高识别率
4. Grok API 可选，但能显著提高复杂简历的识别准确度

## 💡 技术栈

- **后端**: Flask
- **数据库**: SQLite
- **PDF处理**: PyMuPDF (fitz)
- **OCR**: PyMuPDF OCR 功能
- **AI识别**: Grok Vision API
- **前端**: 原生 HTML/CSS/JavaScript

## 📞 问题反馈

如有问题或建议，请在项目仓库提出 Issue。

---

**版本**: 线上部署版 1.0  
**最后更新**: 2025年10月

