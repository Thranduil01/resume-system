# 🐍 Python 版本兼容性说明

## ⚠️ 重要提示

**如果你的 Python 版本是 3.13，可能会遇到依赖安装失败的问题。**

---

## 🔍 为什么会有兼容性问题？

Python 3.13 是 **2024年10月刚发布的最新版本**，一些第三方库还没来得及完全适配。

### 可能出问题的依赖

| 库名 | 风险等级 | 问题原因 |
|------|---------|---------|
| **PyMuPDF** | 🔴 高 | 需要编译 C 扩展，可能编译失败 |
| **Pillow** | 🟡 中 | 旧版本不支持，需要 10.3.0+ |
| **pdfplumber** | 🟡 中 | 依赖 Pillow，间接受影响 |
| Flask | 🟢 低 | 通常没问题 |
| requests | 🟢 低 | 通常没问题 |

---

## ✅ 解决方案（3选1）

### 方案1：使用推荐的 Python 版本 ⭐⭐⭐⭐⭐

**最稳定的方案！**

下载并安装 **Python 3.12** 或 **Python 3.11**：
- 官网：https://www.python.org/downloads/
- macOS 用户：下载 `.pkg` 安装包
- Windows 用户：下载 `.exe` 安装包

**推荐版本**：
- ✅ Python 3.12.6（2024年9月发布，非常稳定）
- ✅ Python 3.11.10（长期支持版本）

安装后重新运行启动脚本即可。

---

### 方案2：手动安装最新兼容版本 ⭐⭐⭐⭐

**适合 Python 3.13 用户**

打开终端（Terminal / 命令提示符），运行：

```bash
# macOS/Linux
cd "/path/to/1030 intern_email_address"
pip3 install Flask pdfplumber Werkzeug Pillow PyMuPDF requests

# Windows
cd "C:\path\to\1030 intern_email_address"
pip install Flask pdfplumber Werkzeug Pillow PyMuPDF requests
```

然后再运行启动脚本。

---

### 方案3：使用兼容配置文件 ⭐⭐⭐

**系统会自动尝试**

项目中包含 `requirements-compatible.txt`，启动脚本会自动使用它来安装兼容版本。

如果还是失败，回到方案1或方案2。

---

## 🎯 推荐步骤

### 如果你是新手

1. **下载 Python 3.12**（不要用 3.13）
2. 安装
3. 双击启动脚本

### 如果你已经有 Python 3.13

**先试试手动安装**：
```bash
pip3 install Flask pdfplumber Werkzeug Pillow PyMuPDF requests
```

如果还是失败，卸载 Python 3.13，安装 Python 3.12。

---

## 📋 各版本兼容性对照表

| Python 版本 | 状态 | 说明 |
|------------|------|------|
| **Python 3.13** | ⚠️ 新版 | 部分库未适配，可能有问题 |
| **Python 3.12** | ✅ 推荐 | 最稳定，完全兼容 |
| **Python 3.11** | ✅ 推荐 | 长期支持，完全兼容 |
| Python 3.10 | ✅ 可用 | 兼容性好 |
| Python 3.9 | ✅ 可用 | 兼容性好 |
| Python 3.8 | ✅ 可用 | 最低支持版本 |
| Python 3.7 及以下 | ❌ 不支持 | 太旧，不推荐 |

---

## 🔧 常见错误信息

### 错误1：KeyError: '__version__'
```
KeyError: '__version__'
```
**原因**：Pillow 版本太旧，不支持 Python 3.13

**解决**：
```bash
pip3 install --upgrade Pillow
```

---

### 错误2：编译失败
```
error: command 'clang' failed
error: subprocess-exited-with-error
```
**原因**：PyMuPDF 编译失败

**解决**：
```bash
# 方法1：安装预编译版本
pip3 install --upgrade PyMuPDF

# 方法2：如果还不行，换 Python 3.12
```

---

### 错误3：ModuleNotFoundError
```
ModuleNotFoundError: No module named 'flask'
```
**原因**：依赖安装不完整（通常是前面某个库安装失败导致）

**解决**：
```bash
# 手动安装
pip3 install Flask pdfplumber Werkzeug Pillow PyMuPDF requests
```

---

## 💡 最佳实践

1. **使用 Python 3.12**（最稳定）
2. 保持 pip 最新：`pip3 install --upgrade pip`
3. 如果遇到问题，先尝试 `pip3 install --upgrade <package>`
4. 实在不行，换 Python 版本

---

## ❓ 常见问题

### Q: 我必须降级 Python 吗？
**A**: 不一定，可以先试试方案2手动安装。90%的情况下能成功。

### Q: 我的电脑上能同时有多个 Python 版本吗？
**A**: 可以！macOS 和 Windows 都支持多版本共存。

### Q: 怎么卸载 Python 3.13？
**A**: 
- **macOS**: 在"应用程序"里找到 Python 3.13 并删除
- **Windows**: 在"设置→应用"里卸载

### Q: 如果所有方法都不行？
**A**: 联系技术支持，提供完整的错误信息截图。

---

## 🚀 快速修复命令（复制粘贴）

### macOS/Linux
```bash
# 更新 pip
pip3 install --upgrade pip

# 安装依赖（不限版本）
pip3 install Flask pdfplumber Werkzeug Pillow PyMuPDF requests

# 如果网络慢，用国内镜像
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple Flask pdfplumber Werkzeug Pillow PyMuPDF requests
```

### Windows
```batch
REM 更新 pip
pip install --upgrade pip

REM 安装依赖
pip install Flask pdfplumber Werkzeug Pillow PyMuPDF requests

REM 如果网络慢，用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple Flask pdfplumber Werkzeug Pillow PyMuPDF requests
```

---

## 📞 需要帮助？

如果按照上述步骤还是无法解决：

1. 截图完整的错误信息
2. 运行 `python3 --version` 查看版本
3. 运行 `pip3 --version` 查看 pip 版本
4. 将上述信息反馈

---

**总结：Python 3.12 是最稳定的选择！** 🎯

