# 快速启动脚本说明

## 📌 概述

提供两种快速启动 FileGather Pro v2.3.5.1 的方法：

### 方式 1：PowerShell 脚本（推荐）

**文件**: `run.ps1`

**使用方法**:
```powershell
.\run.ps1
```

**优点**:
- 更详细的启动信息和错误提示
- 支持彩色输出
- 更专业的界面

**注意**: 如果遇到执行策略限制，请运行：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### 方式 2：批处理脚本

**文件**: `run.bat`

**使用方法**:
1. 直接双击 `run.bat` 文件运行
2. 或在命令提示符中执行：`run.bat`

**优点**:
- 无需配置执行策略
- 任何 Windows 系统都可直接运行
- 适合非开发人员使用

---

## 🔧 前置要求

1. **Python 3.11** 已安装
2. **虚拟环境已创建**: `.venv311`
   ```bash
   python -m venv .venv311
   ```
3. **依赖已安装**:
   ```bash
   .venv311\Scripts\pip install -r requirements.txt
   ```

如果没有依赖列表，请手动安装必需的包：
```bash
.venv311\Scripts\pip install PyQt5==5.15.11 reportlab==4.4.5 PyMuPDF==1.26.6 python-docx==1.2.0 openpyxl==3.1.5 Pillow==10.4.0
```

---

## 🚀 快速开始

### Linux / macOS / PowerShell:
```bash
./run.ps1
```

### Windows 命令提示符 / 直接双击:
```cmd
run.bat
```

---

## 📝 脚本功能

两个脚本都会：

1. ✓ 检查虚拟环境是否存在
2. ✓ 检查主文件是否存在
3. ✓ 自动激活虚拟环境
4. ✓ 启动 FileGather Pro 应用
5. ✓ 显示运行状态信息

---

## ⚠️ 常见问题

### Q: 执行 PowerShell 脚本时出现 "不允许执行脚本" 错误

**A**: 执行以下命令允许本地脚本执行：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q: 双击 run.bat 没有反应

**A**: 
1. 确保虚拟环境已创建在 `.venv311` 目录
2. 确保 Python 已安装且可从命令行访问
3. 打开命令提示符并手动运行 `run.bat` 查看错误信息

### Q: 应用启动后立即关闭

**A**: 检查是否有 Python 错误。运行后查看终端输出信息。

---

## 📦 版本信息

- **应用版本**: 2.3.5.1
- **Python 版本**: 3.11
- **虚拟环境**: .venv311

---

**最后更新**: 2025-11-29
