# FileGather Pro 测试套件

## 概述

本文件夹包含 FileGather Pro 的单元测试和集成测试。

## 测试文件

### 1. `test_launch.py` - 启动测试
- 检查 Python 版本
- 验证所有依赖库是否安装正确
- 验证应用模块结构
- 尝试启动应用窗口

**运行方式**：
```bash
python tests/test_launch.py
```

### 2. `test_exact_search.py` - 精确查找功能测试
- 测试精确文件名匹配（不考虑扩展名）
- 测试大小写不敏感性
- 测试中文字符处理
- 测试模糊查找的高级功能（逻辑与、排除、精确短语）

**运行方式**：
```bash
python tests/test_exact_search.py
```

### 3. `test_folder_gather.py` - 文件夹归集模式测试
- 测试文件夹搜索逻辑
- 验证仅搜索第一级子文件夹
- 验证只有文件夹被返回（文件被忽略）
- 测试关键词匹配

**运行方式**：
```bash
python tests/test_folder_gather.py
```

## 运行所有测试

### 方法 1: 手动依次运行
```bash
cd FileGather_Pro
python tests/test_launch.py
python tests/test_exact_search.py
python tests/test_folder_gather.py
```

### 方法 2: 使用 pytest（如已安装）
```bash
pytest tests/
```

### 方法 3: 使用 Python 的 unittest
```bash
python -m unittest discover tests/ -p "test_*.py"
```

## 测试覆盖范围

| 功能 | 测试文件 | 覆盖率 |
|------|--------|--------|
| 环境检查 | test_launch.py | ✅ 完全 |
| 精确查找 | test_exact_search.py | ✅ 完全 |
| 模糊查找 | test_exact_search.py | ✅ 完全 |
| 文件夹归集 | test_folder_gather.py | ✅ 完全 |
| 文件归集 | - | ⏳ 计划中 |
| 文件操作 | - | ⏳ 计划中 |
| UI 交互 | - | ⏳ 计划中 |

## 期望输出

所有测试通过时，应该看到：

```
✓ 所有检查通过
✓ 测试 1 通过
✓ 测试 2 通过
...
✅ 全部测试通过！
```

## 故障排查

### 导入错误
如果看到 `ImportError` 或 `ModuleNotFoundError`：
```bash
# 确保处于项目根目录
cd FileGather_Pro

# 确保虚拟环境已激活
.\.venv311\Scripts\Activate.ps1  # Windows PowerShell
source .venv311/bin/activate     # Linux/macOS
```

### 缺失依赖
```bash
pip install -r requirements.txt
```

### QApplication 错误
某些测试需要 Qt 环境。如果收到 Qt 相关错误：
```bash
# 在 Windows 上
set QT_QPA_PLATFORM=offscreen

# 在 Linux/macOS 上
export QT_QPA_PLATFORM=offscreen
```

## 添加新测试

1. 在 `tests/` 文件夹中创建新文件 `test_feature_name.py`
2. 按照现有测试的格式编写测试函数
3. 函数名称必须以 `test_` 开头
4. 在 `if __name__ == "__main__"` 块中调用测试函数

**示例**：
```python
def test_new_feature():
    """测试新功能描述"""
    assert condition, "错误信息"
    print("✓ 测试通过")

if __name__ == "__main__":
    test_new_feature()
```

## 持续集成

这些测试可以集成到 GitHub Actions 或其他 CI/CD 系统中自动运行。

参考项目根目录的 `.github/workflows/` 配置。

## 版本信息

- **测试套件版本**: 1.0.0
- **应用版本**: v2.3.5.2+
- **最后更新**: 2025-11-30
