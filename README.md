# FileGather Pro

> 💼 专业文件归集和搜索管理工具

一个功能强大的文件管理工具，用于快速搜索、分类和管理大量文档。支持多格式文件搜索、高级关键词匹配、冲突处理和 PDF 报告生成。

**当前版本**: v2.3.5.1 (2025-11-29)

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
- 现代化 PyQt5 界面
- 即时搜索结果预览
- 右键上下文菜单
- 进度提示和状态反馈

---

## 🚀 快速开始

### 运行程序
```bash
python FileGather_Pro2.3.5.py
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
6. **处理搜索结果**：右键查看文件选项（打开、打开文件夹、复制、删除）
7. **生成报告**：点击"生成 PDF 日志"导出操作记录

---

## 📦 项目结构

### v2.3.5.1 架构（模块化设计 + 精确查找）

```
FileGather_Pro/
├── FileGather_Pro2.3.5.py          # 应用入口（19行）
├── components/                      # 核心模块包
│   ├── __init__.py                  # 包导出接口
│   ├── main_window.py               # 主窗口类（684行）
│   ├── ui_builder.py                # UI构建器（329行）
│   ├── search_logic.py              # 搜索逻辑（121行）
│   ├── file_operations.py           # 文件操作（112行）
│   ├── utils.py                     # 工具函数（75行）
│   ├── dialogs/                     # 对话框子包
│   │   ├── __init__.py
│   │   ├── search_result_dialog.py  # 搜索结果对话框
│   │   ├── conflict_dialog.py       # 冲突处理对话框
│   │   ├── pdf_generator.py         # PDF生成器
│   │   └── README.md
│   └── README.md
├── archive/                         # 旧版本归档
│   ├── FileGather_Pro2.3.4.py
│   ├── FileGather_Pro2.3.4.spec
│   └── README.md
├── .gitignore                       # Git忽略配置
├── LICENSE                          # Apache 2.0 许可证
└── README.md                        # 项目说明
```

### 架构特点
- ✅ **单一职责原则** - 每个模块专注一个功能
- ✅ **低耦合** - 模块之间独立，易于测试
- ✅ **高内聚** - 相关功能集中在同一模块
- ✅ **易扩展** - 添加新功能只需新增模块

---

## 🔧 依赖库

| 库 | 用途 |
|----|------|
| **PyQt5** | GUI 框架 |
| **reportlab** | PDF 生成 |
| **PyMuPDF** | PDF 内容提取 |
| **python-docx** | Word 文件处理 |
| **openpyxl** | Excel 文件处理 |

### 安装依赖
```bash
pip install PyQt5 reportlab PyMuPDF python-docx openpyxl
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
- **components/README.md** - 模块结构说明
- **components/dialogs/README.md** - 对话框包说明

---

## 📝 版本历史

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

## 👤 作者和贡献

**项目名称**: FileGather Pro  
**开发者**: [daiyixr](https://github.com/daiyixr)  
**贡献者**: [ansel333](https://github.com/ansel333) - 代码重构、UI优化、CI/CD工作流  
**创建日期**: 2024年  
**最后更新**: 2025-11-29  

---

## 📞 反馈和支持

如有问题或建议，欢迎：
- 提交 Issue
- 发起 Pull Request
- 联系开发者

---

## 🙏 致谢

感谢以下开源项目的支持：
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - GUI 框架
- [ReportLab](https://www.reportlab.com/) - PDF 生成
- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF 处理
- [python-docx](https://python-docx.readthedocs.io/) - Word 处理
- [openpyxl](https://openpyxl.readthedocs.io/) - Excel 处理

---

**Made with ❤️ for efficient file management**

