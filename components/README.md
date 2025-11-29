# Components 包结构

## 总体架构

FileGather Pro 采用模块化架构，`components` 包包含应用的核心逻辑。

## 目录结构

```
components/
├── __init__.py                 # 包初始化，导出公共接口
├── ui_builder.py               # UI构建器（329行）
├── main_window.py              # 主窗口（684行）
├── search_logic.py             # 搜索逻辑（121行）
├── file_operations.py          # 文件操作（112行）
├── utils.py                    # 工具函数（75行）
├── dialogs/                    # 对话框子包
│   ├── __init__.py             # 包初始化
│   ├── search_result_dialog.py # 搜索结果对话框（60行）
│   ├── conflict_dialog.py      # 冲突处理对话框（200行）
│   ├── pdf_generator.py        # PDF生成器（210行）
│   └── README.md               # 对话框包说明
└── __pycache__/                # Python缓存（git忽略）
```

## 模块职责

### 核心模块

| 模块 | 职责 | 依赖 |
|------|------|------|
| **ui_builder.py** | UI组件创建、样式管理 | PyQt5 |
| **main_window.py** | 应用主控制、信号处理 | 其他所有模块 |
| **search_logic.py** | 搜索算法实现 | utils.py |
| **file_operations.py** | 文件操作（复制、删除、哈希） | utils.py |
| **utils.py** | 工具函数库 | PyQt5, reportlab |
| **dialogs/** | 对话框和报告生成 | ui_builder.py, utils.py |

### 依赖关系

```
main_window.py
    ├─ ui_builder.py
    ├─ search_logic.py ─────► utils.py
    ├─ file_operations.py ──► utils.py
    ├─ dialogs/ ────────────► utils.py
    └─ utils.py
```

## 公共接口（__init__.py）

### 导出的类和函数

```python
# 主应用类
from .main_window import FileGatherPro

# 对话框类
from .dialogs import (
    KeywordSearchResultDialog,
    FileConflictDialog,
    PDFLogGenerator
)

# UI构建器
from .ui_builder import UIBuilder

# 搜索功能
from .search_logic import (
    matches_keyword,
    search_content,
    search_text_file,
    search_pdf,
    search_docx,
    search_excel
)

# 文件操作
from .file_operations import (
    calculate_hash,
    copy_files_without_conflicts,
    copy_selected_files,
    delete_files_batch
)

# 工具函数
from .utils import (
    register_multilingual_fonts,
    format_size,
    wrap_text,
    extract_filename_for_log,
    is_file_locked,
    get_file_info_dict
)
```

## 使用示例

### 导入主应用
```python
from components import FileGatherPro
from PyQt5.QtWidgets import QApplication

app = QApplication([])
window = FileGatherPro()
window.show()
app.exec_()
```

### 搜索文件
```python
from components import matches_keyword, search_content

# 关键词匹配
result = matches_keyword("test", "hello test world")

# 内容搜索
files = search_content("/path/to/folder", "keyword")
```

### 文件操作
```python
from components import copy_selected_files, delete_files_batch

# 复制文件
copy_selected_files(files, target_folder)

# 删除文件
delete_files_batch(files)
```

### 显示对话框
```python
from components import KeywordSearchResultDialog, FileConflictDialog

# 搜索结果对话框
dialog = KeywordSearchResultDialog(parent, results)
dialog.exec_()

# 冲突处理对话框
conflict = FileConflictDialog(parent, files, target)
if conflict.exec_():
    processed_files = conflict.get_selected_files()
```

## 代码统计

| 类别 | 数量 | 行数 |
|------|------|------|
| 模块文件 | 6 | 1491 |
| 对话框文件 | 4 | 482 |
| 总计 | 10 | 1973 |

## 改进点

### 从原始单文件架构升级

✅ **代码组织**: 1686行单文件 → 模块化结构  
✅ **关键点分离**: 对话框单独成包（dialogs/）  
✅ **易读性**: 单个文件平均340行 → 更易理解  
✅ **可维护性**: 明确的职责划分 → 快速定位问题  
✅ **可扩展性**: 清晰的模块边界 → 易于添加功能  
✅ **可测试性**: 独立模块 → 可独立进行单元测试  

## 扩展指南

### 添加新功能

1. **新的搜索格式**
   - 在 `search_logic.py` 中添加 `search_xyz()` 函数
   - 在 `search_content()` 中添加路由

2. **新的对话框**
   - 在 `dialogs/` 中创建 `new_dialog.py`
   - 在 `dialogs/__init__.py` 中导出

3. **新的工具函数**
   - 在 `utils.py` 中添加函数
   - 更新 `components/__init__.py` 导出

---

*最后更新：2025年11月29日*
