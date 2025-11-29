# FileGather Pro 版本档案

## 版本历史与 Git 提交关联

此文件记录每个版本的发布信息、主要改进和对应的 Git 提交。

---

## v2.3.5.1 (2025-11-29)

**发布时间**: 2025-11-29 21:54:51  
**标签**: `2.3.5.1` (待创建)  
**分支**: main

### 主要提交

| 提交哈希 | 提交信息 | 日期 |
|---------|--------|------|
| `7126642` | fix: correct delete button label for accuracy | 2025-11-29 |
| `c2d885b` | feat: add exact filename matching search mode and improve UI layout | 2025-11-29 |
| `5adc9a8` | docs: add ansel333 as co-author and contributor | 2025-11-29 |
| `304964a` | ci: configure workflow to upload exe to GitHub release | 2025-11-29 |

### 新增功能

- ✨ **精确查找模式**: 支持文件名严格匹配
  - 新增 `exact_match_filename()` 函数
  - 添加 `start_exact_search()` 方法
  - 文件名精确匹配（忽略扩展名）

- 🎨 **UI 优化**: 按钮重新排布为三行布局
  - 行1: 🔍 模糊查找 | ✓ 精确查找 | ⏹ 取消搜索
  - 行2: 📂 选择目标 | 📋 开始归集 | 🗑 删除原始文件
  - 行3: 📄 生成日志 | ❓ 使用说明
  - 为所有按钮添加工具提示

- 📚 **文档完善**: 启动脚本和指南
  - `run.ps1`: PowerShell 快速启动脚本
  - `run.bat`: 批处理快速启动脚本
  - `LAUNCH_GUIDE.md`: 完整启动指南

### 技术改进

- 代码文件重构：
  - `search_logic.py`: 添加精确匹配逻辑
  - `ui_builder.py`: 优化按钮布局（9-tuple 返回值）
  - `main_window.py`: 处理精确搜索功能

- 构建工具：
  - `.gitignore`: 添加 `build_2.3.4/` 忽略规则
  - `build_2.3.4/`: v2.3.4 对比版本的构建目录

### 可执行文件

| 文件名 | 大小 | 发布日期 |
|--------|------|---------|
| FileGather_Pro.exe | 70.59 MB | 2025-11-29 21:10:52 |
| FileGather_Pro_2.3.4.exe | 70.44 MB | 2025-11-29 21:54:51 |

### 文件清理

- 重命名: `FileGather_Pro2.3.5.py` → `FileGather_Pro.py`
- 理由: 版本号由代码管理，无需在文件名中重复

---

## v2.3.5 (2025-11-29)

**发布时间**: 2025-11-29 13:00:00  
**标签**: `2.3.5`  
**分支**: main  
**首次提交**: `9448e0b`

### 主要提交

| 提交哈希 | 提交信息 | 日期 |
|---------|--------|------|
| `9448e0b` | refactor: organize AI workflow documentation and finalize v2.3.5 | 2025-11-29 |

### 主要成就

- ✨ **完整模块化重构**: 1686行单文件 → 模块化结构
  - `main_window.py`: 主窗口和搜索逻辑 (832 行)
  - `ui_builder.py`: UI 组件工厂 (444 行)
  - `search_logic.py`: 搜索算法 (121 行)
  - `file_operations.py`: 文件操作 (130 行)
  - `utils.py`: 工具函数 (100 行)
  - `dialogs/`: 对话框子包 (3 个专业模块)

- 📦 **dialogs 包细化**
  - `search_result_dialog.py`
  - `conflict_dialog.py`
  - `pdf_generator.py`

- 🏗️ **项目组织**
  - AI 工作流文档移到 `ai-workflow/`
  - 创建 `archive/` 文件夹归档旧版本
  - 添加 `.gitignore` 配置
  - 创建完整的文档

### 可执行文件

| 文件名 | 大小 | 发布日期 |
|--------|------|---------|
| FileGather_Pro.exe | 67.32 MB | 2025-11-29 13:00:00 |

---

## v2.3.4 (2025-07-17)

**标签**: `2.3.4`  
**分支**: main  
**状态**: 已存档

### 特点

- 单文件结构（1686 行）
- 支持多格式文件搜索（TXT、PDF、DOCX、XLSX）
- 高级关键词匹配语法
- 模糊搜索功能
- PDF 报告生成

### 可执行文件

| 文件名 | 大小 |
|--------|------|
| FileGather_Pro_2.3.4.exe | 70.44 MB |

---

## 版本比较总结

| 特性 | v2.3.4 | v2.3.5 | v2.3.5.1 |
|------|--------|--------|----------|
| 代码结构 | 单文件(1686行) | 模块化(6个模块) | 模块化(6个模块) |
| 精确查找 | ❌ | ❌ | ✅ |
| 模糊查找 | ✅ | ✅ | ✅ |
| 高级语法 | ✅ | ✅ | ✅ |
| 按钮布局 | 单行 | 单行 | 三行 |
| 工具提示 | ❌ | ❌ | ✅ |
| 快速启动脚本 | ❌ | ❌ | ✅ |
| CI/CD 自动化 | ❌ | ✅ | ✅ |
| 代码可维护性 | 低 | 高 | 高 |

---

## Git 工作流

### 标签创建

```bash
# v2.3.5.1 标签（待创建）
git tag -a 2.3.5.1 -m "Release v2.3.5.1 - Exact search and UI improvements"

# 已存在的标签
git tag 2.3.5
git tag 2.3.4
```

### 检查特定版本代码

```bash
# 查看 v2.3.5.1 代码
git show 2.3.5.1:FileGather_Pro.py

# 查看 v2.3.5 代码
git show 2.3.5:FileGather_Pro2.3.5.py

# 查看 v2.3.4 代码
git show 2.3.4:archive/FileGather_Pro2.3.4.py
```

### 获取历史文件

```bash
# 获取 v2.3.4 版本
git checkout 2.3.4 -- archive/FileGather_Pro2.3.4.py

# 获取 v2.3.5 版本
git checkout 2.3.5 -- FileGather_Pro2.3.5.py
```

---

## 发布流程

对于每个新版本：

1. **代码完成**: 完成所有功能开发和测试
2. **更新文档**: 
   - 更新 `README.md` 版本号和功能说明
   - 更新此文件（VERSION_ARCHIVE.md）的版本信息
3. **创建标签**:
   ```bash
   git tag -a X.X.X -m "Release vX.X.X - Feature description"
   git push origin X.X.X
   ```
4. **创建 Release**:
   - GitHub Release 自动附加可执行文件
   - 包含版本说明和更新日志
5. **更新版本档案**: 添加到此文件

---

**最后更新**: 2025-11-29  
**维护者**: daiyixr, ansel333  
**仓库**: https://github.com/ansel333/FileGather_Pro
