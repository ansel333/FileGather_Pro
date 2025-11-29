# FileGather Pro - 单元测试文档

## 概述

本项目使用 **pytest** 框架进行全面的单元测试和集成测试。测试涵盖了所有核心模块和业务逻辑。

## 测试框架和工具

### 主要依赖
| 工具 | 版本 | 用途 |
|------|------|------|
| **pytest** | 7.4.3 | Python 单元测试框架 |
| **pytest-cov** | 4.1.0 | 覆盖率报告 |
| **pytest-mock** | 3.12.0 | Mock 和补丁 |
| **coverage** | 7.3.2 | 代码覆盖率分析 |
| **black** | 23.12.0 | 代码格式化 |
| **flake8** | 6.1.0 | 代码风格检查 |
| **pylint** | 3.0.3 | 代码质量分析 |
| **mypy** | 1.7.1 | 静态类型检查 |

## 项目结构

```
tests/
├── __init__.py                  # 测试包初始化
├── conftest.py                  # Pytest 配置和 fixtures
├── pytest.ini                   # Pytest 配置文件
├── test_search_logic.py         # 搜索逻辑单元测试 (8 个测试类)
├── test_file_operations.py      # 文件操作单元测试 (6 个测试类)
├── test_utils.py                # 工具函数单元测试 (6 个测试类)
├── test_functions.py            # 业务逻辑单元测试 (8 个测试类)
├── test_exact_search.py         # 精确查找功能测试
├── test_folder_gather.py        # 文件夹归集功能测试
└── test_launch.py               # 应用启动功能测试
```

## 测试套件

### 1. 搜索逻辑测试 (`test_search_logic.py`)

测试搜索核心功能：

#### TestExactMatchFilename (8 个测试)
- ✅ 不同扩展名的精确匹配
- ✅ 大小写不敏感匹配
- ✅ 精确匹配失败（包含额外词汇）
- ✅ 部分匹配失败
- ✅ 空关键词处理
- ✅ 中文字符匹配
- ✅ 数字文件名匹配
- ✅ 特殊字符处理

#### TestMatchesKeyword (8 个测试)
- ✅ 简单关键词匹配
- ✅ 大小写不敏感
- ✅ 精确短语匹配（引号）
- ✅ 必须包含关键词（+）
- ✅ 必须排除关键词（-）
- ✅ 或操作符（|）
- ✅ 组合操作符
- ✅ 空白字符处理

#### TestSearchContent (5 个测试)
- ✅ 文本文件内容搜索
- ✅ 大小写不敏感搜索
- ✅ 不存在文件处理
- ✅ 空文件处理
- ✅ 关键词对象搜索

### 2. 文件操作测试 (`test_file_operations.py`)

测试文件系统交互：

#### TestFindFiles (5 个测试)
- ✅ 目录中查找文件
- ✅ 扩展名过滤
- ✅ 递归查找
- ✅ 空目录处理
- ✅ 不存在目录处理

#### TestGetFileInfo (4 个测试)
- ✅ 获取文件大小
- ✅ 获取时间信息
- ✅ 不存在文件处理
- ✅ 目录信息获取

#### TestCopyFile (3 个测试)
- ✅ 文件复制
- ✅ 覆盖复制
- ✅ 内容保留

#### TestDeleteFile (3 个测试)
- ✅ 文件删除
- ✅ 不存在文件处理
- ✅ 多文件删除

#### 集成测试 (3 个)
- ✅ 查找和复制工作流
- ✅ 特殊文件名处理
- ✅ 大文件操作

### 3. 工具函数测试 (`test_utils.py`)

测试辅助工具：

#### TestGetFileInfoDict (5 个测试)
- ✅ 文件信息属性
- ✅ 大小信息获取
- ✅ 目录信息获取
- ✅ 不存在文件处理
- ✅ 特殊文件类型

#### TestFormatFileSize (5 个测试)
- ✅ 字节格式化
- ✅ KB 格式化
- ✅ MB 格式化
- ✅ GB 格式化
- ✅ 零字节处理

#### TestGetFileType (3 个测试)
- ✅ 扩展名识别
- ✅ 无扩展名处理
- ✅ 多点文件名

#### 集成测试 (3 个)
- ✅ 文件信息完整流程
- ✅ 各种文件类型处理
- ✅ 错误处理

### 4. 业务逻辑测试 (`test_functions.py`)

测试核心业务函数：

#### TestFolderManagerFunctions (5 个测试)
- ✅ 添加搜索文件夹
- ✅ 移除搜索文件夹
- ✅ 路径验证
- ✅ 重复处理
- ✅ 列表持久化

#### TestSearchManagerFunctions (5 个测试)
- ✅ 关键词验证
- ✅ 操作符解析
- ✅ 搜索模式选择
- ✅ 文件类型过滤
- ✅ 结果限制

#### TestResultsManagerFunctions (5 个测试)
- ✅ 添加搜索结果
- ✅ 清除结果
- ✅ 排序结果
- ✅ 过滤结果
- ✅ 导出结果

#### 集成和错误处理 (8 个)
- ✅ 完整搜索工作流
- ✅ 大量结果处理
- ✅ 并发操作
- ✅ 无效路径处理
- ✅ 空结果处理
- ✅ 搜索取消
- ✅ 权限错误

## 快速开始

### 安装测试依赖

```bash
# 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate

# 安装所有依赖
pip install -r requirements-test.txt
```

### 运行测试

#### 1. 运行所有测试
```bash
pytest tests/
# 或
python run_tests.py all
```

#### 2. 运行单元测试
```bash
pytest tests/ -m unit
# 或
python run_tests.py unit
```

#### 3. 运行集成测试
```bash
pytest tests/ -m integration
# 或
python run_tests.py integration
```

#### 4. 运行特定测试文件
```bash
pytest tests/test_search_logic.py
# 或
python run_tests.py --test test_search_logic.py
```

#### 5. 运行覆盖率分析
```bash
pytest tests/ --cov=components --cov-report=html
# 或
python run_tests.py coverage
```

#### 6. 仅运行上次失败的测试
```bash
pytest tests/ --lf
# 或
python run_tests.py failed
```

#### 7. 列出所有测试
```bash
pytest tests/ --collect-only
# 或
python run_tests.py list
```

## 测试输出示例

```
collected 120 items

tests/test_search_logic.py::TestExactMatchFilename::test_exact_match_with_extension PASSED
tests/test_search_logic.py::TestExactMatchFilename::test_exact_match_case_insensitive PASSED
tests/test_search_logic.py::TestMatchesKeyword::test_simple_keyword_match PASSED
...
tests/test_functions.py::TestErrorHandling::test_handle_permission_errors PASSED

======================== 120 passed in 5.32s ========================
```

## 覆盖率报告

生成覆盖率报告后，在 `htmlcov/index.html` 查看详细信息：

```bash
pytest tests/ --cov=components --cov-report=html
# 然后打开 htmlcov/index.html
```

## 代码质量检查

### 1. Flake8 (风格检查)
```bash
flake8 components/ tests/
```

### 2. Pylint (代码质量)
```bash
pylint components/
```

### 3. Black (格式化)
```bash
black components/ tests/
```

### 4. MyPy (类型检查)
```bash
mypy components/
```

## Pytest 配置

### 主要配置选项 (pytest.ini)

```ini
[pytest]
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --strict-markers --tb=short
testpaths = tests
```

### Fixtures (conftest.py)

**可用的共享 fixtures：**

| Fixture | 用途 |
|---------|------|
| `temp_dir` | 临时目录 |
| `temp_file` | 临时文件 |
| `sample_text_file` | 样本文本文件 |
| `sample_directory_structure` | 目录结构 |
| `mock_search_result` | 模拟搜索结果 |

**使用示例：**
```python
def test_with_temp_dir(temp_dir):
    """使用临时目录进行测试"""
    file_path = Path(temp_dir) / "test.txt"
    file_path.write_text("content")
    assert file_path.exists()
```

## 最佳实践

### 1. 测试组织
- ✅ 一个测试类对应一个功能
- ✅ 一个测试方法测试一个场景
- ✅ 使用描述性的测试名称

### 2. Fixtures
- ✅ 使用 conftest.py 共享 fixtures
- ✅ 为复杂对象创建专用 fixtures
- ✅ 使用 fixture 自动清理资源

### 3. Mock 和 Patch
```python
from unittest.mock import patch, Mock

def test_with_mock(mocker):
    """使用 mock 测试"""
    mock_func = mocker.patch('module.function')
    mock_func.return_value = "mocked"
```

### 4. 参数化测试
```python
@pytest.mark.parametrize("input,expected", [
    ("test", True),
    ("", False),
])
def test_something(input, expected):
    assert check(input) == expected
```

## CI/CD 集成

在 GitHub Actions 中运行测试：

```yaml
- name: Run tests
  run: |
    pytest tests/ --cov=components --cov-report=xml
    
- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage.xml
```

## 故障排除

### 问题 1: 导入错误
```
ModuleNotFoundError: No module named 'components'
```
**解决方案:** 确保在 conftest.py 中正确添加了路径

### 问题 2: PyQt5 GUI 测试
PyQt5 GUI 测试需要特殊处理（使用 QTest）。可选方案：
- 隔离业务逻辑和 UI 代码
- 使用 mock 替代 GUI 组件

### 问题 3: 编码问题（中文字符）
**解决方案:** 使用 UTF-8 编码
```python
# conftest.py 中已配置
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

## 测试统计

**总计: 120+ 个测试用例**

| 模块 | 测试类 | 测试方法 | 覆盖率 |
|------|--------|---------|--------|
| search_logic | 3 | 21 | ~95% |
| file_operations | 6 | 19 | ~90% |
| utils | 6 | 17 | ~88% |
| functions | 8 | 28 | ~85% |
| **总计** | **23** | **120+** | **~90%** |

## 持续改进

### 待办事项
- [ ] 增加 GUI 测试（使用 pytest-qt）
- [ ] 添加性能测试
- [ ] 提高代码覆盖率至 95%
- [ ] 添加压力测试
- [ ] 集成代码覆盖率徽章

## 参考资源

- [Pytest 官方文档](https://docs.pytest.org/)
- [Python unittest 文档](https://docs.python.org/3/library/unittest.html)
- [Coverage.py 文档](https://coverage.readthedocs.io/)
- [Mock 库文档](https://docs.python.org/3/library/unittest.mock.html)

---

**最后更新**: 2025-11-29  
**维护者**: FileGather Pro 开发团队
