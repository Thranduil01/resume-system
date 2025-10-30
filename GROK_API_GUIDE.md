# Grok API 使用指南

## 🤖 什么是 Grok API？

Grok 是 xAI 开发的先进 AI 模型，支持视觉理解能力。使用 Grok API 可以：
- 智能识别简历中的文本（即使是扫描版或图片）
- 理解上下文，更准确地提取信息
- 无需本地安装 OCR 软件

## 📝 获取 Grok API Key

1. 访问 xAI 官网：https://x.ai
2. 注册账号并登录
3. 进入 API 控制台
4. 创建新的 API Key
5. 复制 API Key（格式类似：`xai-xxxxxxxxxxxxxx`）

## 💰 费用说明

Grok API 是付费服务，按使用量计费：
- Grok Vision Beta: 约 $X/百万 tokens（具体价格请查看官网）
- 建议先小批量测试，确认效果后再大规模使用

## 🔧 使用方法

### 方法1：网页界面使用

1. 启动系统：`python3 app.py`
2. 打开浏览器：`http://127.0.0.1:5001`
3. 在"Grok API Key"输入框中输入您的 API Key
4. 点击"开始解析"
5. 系统会自动使用 Grok API 识别无法通过文本/OCR 提取的简历

### 方法2：环境变量配置

您也可以将 API Key 设置为环境变量，避免每次输入：

**macOS/Linux:**
```bash
export GROK_API_KEY="xai-your-api-key-here"
python3 app.py
```

**Windows:**
```powershell
set GROK_API_KEY=xai-your-api-key-here
python app.py
```

然后修改 `app.py`，从环境变量读取：
```python
import os
grok_api_key = data.get('grok_api_key') or os.getenv('GROK_API_KEY')
```

## 🎯 识别策略

系统采用**三级智能识别**：

1. **第一级：文本提取**（免费，速度快）
   - 适用于正常的文本型 PDF
   
2. **第二级：OCR 识别**（免费，需要安装 Tesseract）
   - 适用于扫描版 PDF
   - 识别准确率 70-90%
   
3. **第三级：Grok API**（付费，最强大）
   - 适用于所有类型的 PDF
   - AI 理解能力，识别准确率 90-98%
   - 可以理解复杂布局和手写字体

只有当前一级方法失败时，才会尝试下一级方法，节省 API 调用成本。

## 📊 Grok API 优势

相比 OCR：
- ✅ 无需本地安装软件
- ✅ 支持复杂布局识别
- ✅ 理解上下文语义
- ✅ 支持手写字体
- ✅ 多语言混合识别
- ✅ 自动纠错

相比纯文本提取：
- ✅ 可以处理扫描版 PDF
- ✅ 可以处理图片格式简历
- ✅ 可以理解表格和非标准布局

## 💡 使用建议

### 推荐使用场景：
- 处理大量扫描版简历
- 需要高准确率的场景
- 简历格式复杂、布局不规则
- 包含手写内容的简历

### 不推荐使用场景：
- 普通文本 PDF（用文本提取即可）
- 预算有限（可以先用 OCR）
- 简历数量很少（手动提取可能更快）

### 节省成本的技巧：
1. 只对文本提取失败的 PDF 使用 Grok API
2. 批量处理时，先测试几个样本
3. 如果数据不敏感，可以考虑其他免费 OCR 方案
4. 定期检查 API 使用量

## 🔒 安全提示

- ⚠️ 不要将 API Key 提交到 Git 仓库
- ⚠️ 不要在公开的代码中硬编码 API Key
- ⚠️ 定期轮换 API Key
- ⚠️ 注意简历中可能包含敏感信息

## 🆚 OCR vs Grok API 对比

| 特性 | OCR (Tesseract) | Grok API |
|------|-----------------|----------|
| 成本 | 免费 | 付费 |
| 安装 | 需要安装软件 | 无需安装 |
| 准确率 | 70-90% | 90-98% |
| 速度 | 较慢 | 较快 |
| 复杂布局 | 一般 | 优秀 |
| 手写识别 | 较差 | 优秀 |
| 语义理解 | 无 | 有 |
| 网络要求 | 无 | 需要联网 |

## 📞 支持

遇到问题？
- 查看 xAI 官方文档：https://docs.x.ai
- 检查 API Key 是否有效
- 确认账户余额是否充足
- 查看系统日志中的错误信息

## 🎉 开始使用

现在就试试 Grok API，体验 AI 驱动的简历信息提取！

```bash
# 安装依赖
pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# 启动系统
python3 app.py

# 在浏览器中输入您的 Grok API Key，开始解析！
```

