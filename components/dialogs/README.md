# Dialogs 包结构

## 概述

`dialogs` 包将原来的单个 `dialogs.py` 文件按功能拆分成多个专用模块，提高代码的可读性和可维护性。

## 模块说明

### 1. `search_result_dialog.py` (60 行)
**关键词搜索结果对话框**

- **类**: `KeywordSearchResultDialog`
- **功能**: 显示关键词搜索结果的树形视图
- **用途**: 在完成搜索后显示每个关键词的匹配文件
- **特点**:
  - 树形结构展示关键词和对应的文件
  - 灰色显示未找到结果的关键词
  - 支持自动展开所有节点

### 2. `conflict_dialog.py` (200 行)
**文件冲突处理对话框**

- **类**: `FileConflictDialog`
- **功能**: 处理文件复制时的覆盖、跳过、重命名等冲突解决方案
- **用途**: 当目标文件夹中已存在同名文件时，提供多种处理选项
- **特点**:
  - 支持单个文件操作和批量操作
  - 自动生成唯一的文件名
  - 彩色标记不同的处理状态
  - 包含"全部覆盖"和"全部重命名"快捷操作

### 3. `pdf_generator.py` (210 行)
**PDF日志生成器**

- **类**: `PDFLogGenerator`
- **功能**: 生成包含搜索结果和操作记录的PDF文档
- **用途**: 导出搜索过程和操作结果为PDF报告
- **特点**:
  - 支持选择导出条数（前20条、前50条、全部）
  - 包含基本信息表、操作记录、文件列表等多个部分
  - 使用中文字体支持
  - 自动生成结构化的PDF表格

### 4. `__init__.py` (12 行)
**包初始化文件**

- **功能**: 定义包的公共接口
- **导出类**:
  - `KeywordSearchResultDialog`
  - `FileConflictDialog`
  - `PDFLogGenerator`

## 导入方式

### 之前（单文件）
```python
from .dialogs import KeywordSearchResultDialog, FileConflictDialog, PDFLogGenerator
```

### 现在（多文件包）
```python
# 方式1：从包导入（推荐）
from .dialogs import KeywordSearchResultDialog, FileConflictDialog, PDFLogGenerator

# 方式2：从具体模块导入
from .dialogs.search_result_dialog import KeywordSearchResultDialog
from .dialogs.conflict_dialog import FileConflictDialog
from .dialogs.pdf_generator import PDFLogGenerator
```

**两种方式都能正常工作**，因为 `__init__.py` 已经进行了导出。

## 文件大小变化

| 文件 | 行数 |
|------|------|
| 原 dialogs.py | 384 |
| 新 search_result_dialog.py | 60 |
| 新 conflict_dialog.py | 200 |
| 新 pdf_generator.py | 210 |
| 新 __init__.py | 12 |
| **总计** | **482** |

**说明**: 行数略有增加是因为添加了更详细的文档字符串和代码注释。

## 优势

✅ **更高的内聚性**：每个模块专注于一个功能  
✅ **更好的可读性**：缩小每个文件的范围  
✅ **更易维护**：修改一个对话框只需改一个文件  
✅ **更易测试**：可以独立测试每个对话框  
✅ **更易扩展**：添加新对话框只需新增一个文件  

## 后续扩展

如果需要添加新的对话框，只需：

1. 在 `dialogs` 文件夹中创建新文件，如 `new_dialog.py`
2. 在文件中定义对话框类
3. 在 `__init__.py` 中添加导入和导出

```python
# dialogs/__init__.py
from .new_dialog import NewDialog
__all__ = [
    'KeywordSearchResultDialog',
    'FileConflictDialog',
    'PDFLogGenerator',
    'NewDialog',  # 新增
]
```

---

*最后更新：2025年11月29日*
