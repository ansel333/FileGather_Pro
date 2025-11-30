# FileGather Pro

> 💼 专业文件归集和搜索管理工具

一个功能强大的文件管理工具，用于快速搜索、分类和管理大量文档。支持多格式文件搜索、高级关键词匹配、冲突处理和 PDF 报告生成。

**当前版本**: v2.5.0 (2025-11-30)

🌐 **Other Languages**: [English](README.md)

---

## ✨ 主要功能

### 🔍 高级搜索
- **两种查找模式**：
  - **模糊查找**（默认）：搜索文件名中包含关键词的文件
  - **精确查找**：搜索文件名严格对应关键词的文件
- **高级关键词语法**：`+keyword`、`-keyword`、`|`、`*`、`"exact phrase"`
- **多格式支持**：TXT、PDF、DOCX、XLSX

### 📁 文件管理
- 添加/删除搜索文件夹
- 支持本地磁盘和网络路径
- 批量复制和删除文件
- 智能冲突处理（覆盖、跳过、重命名）

### 📊 报告生成
- 生成 PDF 操作日志
- 包含搜索条件、操作记录、文件列表
- 支持选择导出条数（前20条、前50条、全部）
- 中文字体支持

### 🎨 用户界面
- 现代化 PyQt6 界面（6.7.1）
- 白色背景+彩色边框按钮设计
- 单行紧凑按钮布局
- 即时搜索结果预览
- 右键上下文菜单
- 进度提示和状态反馈
- 条件可见的取消按钮

---

## 🚀 快速开始

### 运行程序
```bash
python FileGather_Pro.py
```

### 或使用可执行文件
```bash
FileGather_Pro.exe  # Windows 可执行文件（包含自定义图标）
```

### 基本使用流程
1. **启动程序**：运行主程序文件启动应用
2. **添加搜索文件夹**：点击"添加文件夹"按钮选择要搜索的目录
3. **输入搜索条件**：输入关键词或文件名
4. **选择搜索类型**：
   - 🔍 **模糊查找**：搜索包含关键词的文件（支持高级语法）
   - ✓ **精确查找**：搜索文件名完全匹配的文件
5. **开始搜索**：点击对应的搜索按钮
6. **查看结果**：搜索结果显示在下方表格中
7. **处理文件**：右键或使用按钮进行复制、删除等操作
8. **生成报告**：点击"生成 PDF 日志"导出操作记录

---

## 🧪 测试

### 安装
```bash
# 安装测试依赖
pip install -r requirements-test.txt
```

### 运行测试
```bash
# 运行所有测试（47+ 个测试通过）
$env:QT_QPA_PLATFORM='offscreen'
python -m pytest tests/ -v

# 运行特定测试类别
python -m pytest tests/test_file_operations.py -v    # 文件/文件夹操作（11 个测试）
python -m pytest tests/test_pyqt6_dialogs.py -v      # PyQt6 枚举处理（12 个测试）
python -m pytest tests/test_gather_mode_routing.py -v # gather_mode 路由（14 个测试）
python -m pytest tests/test_search_logic.py -v       # 搜索逻辑（20 个测试）

# 运行并生成覆盖率报告
python -m pytest tests/ --cov=components --cov-report=html

# 仅运行单元测试
python -m pytest tests/ -m unit -v

# 使用测试运行脚本
python run_tests.py all           # 运行所有测试
python run_tests.py unit          # 仅运行单元测试
python run_tests.py coverage      # 生成覆盖率报告
python run_tests.py list          # 列出所有可用测试
```

### 测试覆盖
- **11 个测试** in `test_file_operations.py` - 文件/文件夹复制、删除、批量操作、哈希计算
- **12 个测试** in `test_pyqt6_dialogs.py` - PyQt6 枚举处理、对话框返回值、按钮组合
- **14 个测试** in `test_gather_mode_routing.py` - 文件/文件夹模式路由、条件逻辑、操作
- **20 个测试** in `test_search_logic.py` - 精确匹配、关键词匹配、内容搜索
- **47+ 总测试** 全部通过，覆盖范围全面
- 环境：Python 3.11.9、pytest 7.4.3、PyQt6 6.7.1

---

## 📦 项目结构

### v2.4.0 架构（模块化 + 功能扩展 + 自动化构建）

```
FileGather_Pro/
├── FileGather_Pro.py                # 应用入口（v2.5.0）
├── FileGather_Pro.spec              # PyInstaller 配置
├── app.ico                          # 应用程序图标（256×256）
├── components/                      # 核心模块包
│   ├── __init__.py
│   ├── main_window.py               # 主窗口类（167行，-85%）
│   ├── ui_builder.py                # UI构建器
│   ├── search_logic.py              # 搜索逻辑
│   ├── file_operations.py           # 文件操作
│   ├── utils.py                     # 工具函数
│   ├── dialogs/                     # 对话框子包
│   │   ├── __init__.py
│   │   ├── search_result_dialog.py  # 搜索结果对话框
│   │   ├── conflict_dialog.py       # 冲突处理对话框
│   │   ├── pdf_generator.py         # PDF生成器
│   │   └── README.md
│   ├── functions/                   # 业务逻辑模块（28+ 函数）
│   │   ├── __init__.py
│   │   ├── folder_manager.py        # 文件夹管理
│   │   ├── search_manager.py        # 搜索管理
│   │   ├── results_manager.py       # 结果管理
│   │   ├── search_operations.py     # 搜索操作
│   │   ├── file_operations_ui.py    # UI文件操作
│   │   ├── ui_interactions.py       # UI交互
│   │   └── README.md
│   └── README.md
├── tests/                           # 测试套件（47+ 个测试）
├── archive/                         # 旧版本归档
├── ai-workflow/                     # 工作流文档
├── .github/workflows/               # GitHub Actions CI/CD
│   └── build-all-platforms.yml      # 多平台自动构建
├── .gitignore                       # Git忽略配置
├── LICENSE                          # Apache 2.0 许可证
└── README.md                        # 项目说明
```

### 架构特点
- ✅ **单一职责原则** - 每个模块专注一个功能
- ✅ **低耦合** - 模块之间独立，易于测试
- ✅ **高内聚** - 相关功能集中在同一模块
- ✅ **易扩展** - 添加新功能只需新增模块
- ✅ **85% 代码精简** - 主窗口从 1090 行减至 167 行
- ✅ **专业图标** - 256×256 多分辨率图标集成
- ✅ **自动化构建** - GitHub Actions CI/CD 工作流
- ✅ **完整测试** - 47+ 个测试用例全部通过

---

## 🔧 依赖库

| 库 | 用途 |
|----|------|
| **PyQt6** | GUI 框架 (6.7.1) |
| **reportlab** | PDF 生成 |
| **PyMuPDF** | PDF 内容提取 |
| **python-docx** | Word 文件处理 |
| **openpyxl** | Excel 文件处理 |
| **Pillow** | 图像处理和图标生成 |

### 安装依赖
```bash
pip install PyQt6==6.7.1 reportlab==4.4.5 PyMuPDF==1.26.6 python-docx==1.2.0 openpyxl==3.1.5 Pillow==10.4.0
```

### 从可执行文件运行（推荐）
```bash
# 无需安装任何依赖，直接运行
./FileGather_Pro.exe
```

---

## 🚨 注意事项

### 性能建议
- 大规模搜索：先通过文件名过滤
- 内容搜索：比文件名搜索耗时更长，请耐心等待
- 网络路径：速度可能较慢，建议先映射本地驱动器

### 安全提示
- ⚠️ 删除操作**不可撤销**，请确认后再执行
- ⚠️ 仅用于合法的文件管理操作
- ⚠️ 避免对系统文件或受保护文件进行不当操作
- ⚠️ 建议定期备份重要文件

---

## 📚 文档

- **REFACTORING.md** - 重构详细说明和架构设计
- **DIALOGS_REFACTORING.md** - 对话框包拆分说明
- **QUICK_REFERENCE.md** - 快速参考指南
- **.github/WORKFLOWS_GUIDE.md** - 详细的 CI/CD 工作流指南
- **.github/BUILD_GUIDE.md** - 多平台构建快速参考
- **components/README.md** - 模块结构说明
- **components/dialogs/README.md** - 对话框包说明

---

## 📝 版本历史

### 🎉 v2.5.0 (2025-11-30) - 版本源管理与多平台发布
**重大改进**：
- 🔄 **统一版本源**
  - 创建 `VERSION` 文件作为唯一版本源
  - 所有代码和工作流从 `VERSION` 文件读取版本号
  - 无需重复修改多个文件，提高维护效率
  
- 🚀 **多平台 CI/CD 优化**
  - 所有工作流已更新为从 `VERSION` 文件读取版本
  - 支持 4 个构建平台：Windows 11、macOS Intel、macOS ARM64、Linux .deb
  - 工作流自动创建 GitHub Release
  - 标签推送后自动触发并行构建
  
- 📋 **项目文档完善**
  - 添加 `PROJECT_NAVIGATION.md` - 项目导航指南
  - 添加 `PROJECT_COMPLETION_REPORT.md` - 完整项目报告
  - 添加 `CLEANUP_SUMMARY.md` - 清理总结文档
  - 所有文档已更新至最新版本
  
- 🧹 **项目清理**
  - 删除重复的工作流文件（仅保留 build-all-platforms.yml）
  - 移除过时的工作流配置
  - 所有过时文件已清理

**技术细节**:
- VERSION 文件：集中管理版本号
- main_window.py：动态读取版本号
- 工作流：改为从 VERSION 文件提取版本
- 47+ 单元测试全部通过
- 1 个统一的 GitHub Actions 工作流

### 🎉 v2.4.0 (2025-11-29) - 主窗口精简与图标集成 & PyQt6 升级
**重大改进**：
- 🔧 **主窗口重构**：代码行数从 1090 行精简至 167 行（-85%）
  - 删除 29 个重复方法
  - 提取全部业务逻辑到 functions/ 模块
  - 保留 5 个核心框架方法
  
- 🎨 **专业图标集成**
  - 集成 256×256 多分辨率应用图标
  - 在 File Explorer、Start Menu、Taskbar 中完美显示
  - PyInstaller 自动嵌入图标到可执行文件
  
- 🔧 **PyQt6 升级**
  - 升级框架从 PyQt5 5.15.11 到 PyQt6 6.7.1
  - 修复 20+ PyQt6 枚举常数（AlignmentFlag、ItemDataRole、SelectionMode 等）
  - 更新对话框 exec() 调用和 StandardButton 枚举
  - 优化按钮样式：白色背景 + 彩色边框 + 悬停效果
  - 添加条件可见的取消按钮（搜索时显示）
  
- 📝 **测试覆盖增强**
  - 添加 11 个文件/文件夹操作测试
  - 添加 12 个 PyQt6 枚举处理测试
  - 添加 14 个 gather_mode 路由测试
  - 总计 47+ 单元测试，全部通过
  - 验证文件夹复制/删除功能
  - 验证条件路由逻辑
  
- 🔄 **多平台构建优化**
  - Windows 11 (Intel x64) 自动构建
  - macOS Intel x86_64 和 Apple Silicon ARM64 并行构建
  - Linux 创建 .deb 安装包
  - 标签发布时自动创建 GitHub Release
  
- 📦 **项目清理**
  - 移除临时构建文件和脚本
  - 保留生产必需的核心文件
  - 工作区精简化

**技术细节**:
- components/main_window.py：167 行（框架代码）
- components/functions/：28+ 个业务逻辑函数
- PyQt6 6.7.1 框架升级（从 5.15.11）
- 47+ 单元测试，comprehensive coverage
- PyInstaller v6.17.0 配置
- GitHub Actions 多平台自动构建

### ✨ v2.3.5.1 (2025-11-29) - 精确查找功能
**新增功能**：
- 🎯 **精确查找模式**
  - 新增"✓ 精确查找"按钮，支持文件名严格匹配
  - 精确查找忽略文件扩展名，只匹配文件名主体
  - 例如：关键词"报告"只会匹配"报告.xlsx"、"报告.pdf"等，不会匹配"年度报告.docx"

- 🎨 **UI 优化**
  - 重新排布按钮为三行布局，更加美观直观
  - 第一行：🔍 模糊查找 | ✓ 精确查找 | ⏹ 取消搜索
  - 第二行：📂 选择目标 | 📋 开始归集 | 🗑 删除原文
  - 第三行：📄 生成日志 | ❓ 使用说明
  - 添加工具提示（Tooltips）说明各按钮功能

- 🔍 **搜索逻辑改进**
  - `search_logic.py` 添加 `exact_match_filename()` 函数
  - 精确查找使用专门的匹配逻辑，不支持高级语法（仅基本关键词）
  - 模糊查找保持所有高级功能（逻辑与/或、排除、通配符等）

**技术改进**：
- 拆分搜索逻辑：`start_search()` 处理模糊查找，`start_exact_search()` 处理精确查找
- 代码复用：共享文件遍历、大小/日期筛选等逻辑

### 🎯 v2.3.5 (2025-11-29) - 完整模块化重构
**主要改进**：
- ✨ **架构重构**：1686行单文件 → 模块化结构
  - 平均文件大小 340 行，便于维护
  - 单一职责原则，清晰的模块边界
  
- 📦 **dialogs 包细化**：拆分为多个专业模块
  - `search_result_dialog.py` - 搜索结果展示（60行）
  - `conflict_dialog.py` - 冲突处理（200行）
  - `pdf_generator.py` - PDF 报告生成（210行）
  
- 📚 **文档完善**：
  - REFACTORING.md - 重构详细说明
  - DIALOGS_REFACTORING.md - 对话框拆分报告
  - components/README.md - 模块结构说明
  - QUICK_REFERENCE.md - 快速参考指南
  
- 🏗️ **项目整理**：
  - 创建 archive 文件夹归档旧版本
  - 添加 .gitignore 文件（支持 Python、IDE、编译产物）
  - 清理 build/ 和 dist/ 目录

### v2.3.4 (2025-07-17)
- 优化搜索结果及按钮显示
- 更新应用程序图标为 app.ico
- 修复图标显示问题

### v2.3.3
- 支持多语言、PDF、Word 和 Excel 文件搜索（已弃用）

---

## 🎯 使用场景

- **文档管理**：快速定位公司内部的文档和报告
- **代码搜索**：在大型项目中搜索特定代码片段
- **日志分析**：查找和分析日志文件中的信息
- **内容筛选**：从大量文件中提取满足条件的内容
- **文件整理**：批量复制和组织文件

---

## 📄 许可证

本项目遵循 **Apache 2.0** 许可证。  
有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

---

## 📦 获取可执行文件

### 多平台支持
FileGather Pro 现已支持以下平台的自动构建：
- ✅ **Windows 11** (Intel x64)
- ✅ **macOS** (Intel x86_64 和 Apple Silicon ARM64)
- ✅ **Linux** (Ubuntu/Debian .deb 包)

### GitHub Release 下载
前往 [Releases](https://github.com/ansel333/FileGather_Pro/releases) 页面下载最新版本的可执行文件

**v2.4.0+ 特点**：
- ✅ 跨平台支持（Windows、macOS、Linux）
- ✅ 包含自定义应用图标
- ✅ 优化的代码结构（-85% 代码）
- ✅ 完整的功能特性
- ✅ 无需 Python 环境即可运行

#### Windows
直接运行 `FileGather_Pro.exe`

#### macOS
```bash
chmod +x FileGather_Pro
./FileGather_Pro
```

#### Linux (Debian/Ubuntu)
```bash
sudo dpkg -i filegather-pro_*.deb
filegather-pro
```

---

## 👤 作者和贡献

**项目名称**: FileGather Pro  
**开发者**: [daiyixr](https://github.com/daiyixr)  
**贡献者**: [ansel333](https://github.com/ansel333) - 代码重构、UI优化、CI/CD工作流、图标集成  
**创建日期**: 2024年  
**最后更新**: 2025-11-30  

---

## 📞 反馈和支持

如有问题或建议，欢迎：
- 提交 Issue
- 发起 Pull Request
- 联系开发者

---

## 🙏 致谢

感谢以下开源项目的支持：
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - GUI 框架 (6.7.1)
- [PyInstaller](https://www.pyinstaller.org/) - 可执行文件构建
- [ReportLab](https://www.reportlab.com/) - PDF 生成
- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF 处理
- [python-docx](https://python-docx.readthedocs.io/) - Word 处理
- [openpyxl](https://openpyxl.readthedocs.io/) - Excel 处理
- [Pillow](https://python-pillow.org/) - 图像处理

---

**Made with ❤️ for efficient file management**
