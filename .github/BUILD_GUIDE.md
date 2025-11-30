# 多平台构建快速参考

## 概览

FileGather Pro 现在支持自动构建以下平台的可执行文件：

```
┌─────────────────┬──────────────┬─────────────────────┐
│   Platform      │  Architecture│  Output Format      │
├─────────────────┼──────────────┼─────────────────────┤
│ Windows 11      │ Intel x64    │ .exe                │
│ macOS           │ Intel x86_64 │ Mach-O Binary       │
│ macOS           │ ARM64        │ Mach-O Binary       │
│ Linux/Ubuntu    │ x86_64       │ .deb Package        │
└─────────────────┴──────────────┴─────────────────────┘
```

## 工作流文件

### 推荐使用

#### `build-all-platforms.yml` ⭐
**一次性为所有平台构建**

```bash
# 自动触发（push 到 main）
git commit -m "fix: bug fix"
git push origin main

# 或标记发布（自动创建 GitHub Release）
git tag v2.5.0
git push origin v2.5.0
```

**优点**：
- ✅ 并行构建所有平台
- ✅ 标记时自动创建 Release
- ✅ 统一的版本管理

### 平台专用工作流

#### `build-windows-11-intel.yml`
Windows 11 Intel x64 专用构建

#### `build-macos.yml`
macOS Intel x86_64 和 Apple Silicon ARM64

#### `build-linux-deb.yml`
Linux 创建 .deb 安装包

## 使用场景

### 场景 1：日常开发
```bash
# push 代码到 main 分支
git add .
git commit -m "feat: new feature"
git push origin main

# -> 自动触发 build-all-platforms.yml
# -> 可从 GitHub Actions 页面下载 artifacts
```

### 场景 2：发布新版本
```bash
# 创建版本标签
git tag v2.5.0
git push origin v2.5.0

# -> 自动触发 build-all-platforms.yml
# -> 自动创建 GitHub Release
# -> Release 包含所有平台的可执行文件
```

### 场景 3：手动构建
GitHub Actions 页面 → 选择工作流 → Run workflow

### 场景 4：仅构建某个平台（急速）
选择平台专用工作流手动触发：
- 仅需要 Windows？用 `build-windows-11-intel.yml`
- 仅需要 macOS？用 `build-macos.yml`
- 仅需要 Linux？用 `build-linux-deb.yml`

## 版本管理

### 自动版本提取
工作流从 `FileGather_Pro.py` 中自动提取版本：

```python
# FileGather_Pro.py
class FileGatherPro(QMainWindow):
    """文件归集管理器 2.4.0"""  # ← 版本号从这里提取
```

### 指定版本
```bash
git tag v2.5.0
git push origin v2.5.0
# -> Release 创建，版本为 2.5.0
```

## 构建输出

### 从 GitHub Actions 下载
1. 进入项目 GitHub Actions 页面
2. 选择最近的工作流运行
3. 下载相应的 artifact（30天内可用）

### 从 Release 下载 ⭐
1. 进入项目 Releases 页面
2. 选择相应版本
3. 下载所有平台的可执行文件

## 文件说明

### Windows 输出
- **FileGather_Pro.exe** - 直接运行

### macOS 输出
```bash
# 设置执行权限
chmod +x FileGather_Pro

# 运行
./FileGather_Pro

# 如需签名和公证（Apple 开发者）
codesign -s - FileGather_Pro
```

### Linux 输出
```bash
# 安装 .deb 包
sudo dpkg -i filegather-pro_2.5.0-1_amd64.deb

# 卸载
sudo apt remove filegather-pro

# 运行
filegather-pro
```

## 构建信息

每个构建生成 `BUILD_INFO.txt`：

```
Build Information
=================
Version: 2.4.0
Platform: Windows 11 (Intel/x64)
Build Date: 2025-11-30 12:34:56 UTC
Python Version: 3.11
PyQt6 Version: 6.7.1
```

## 常见问题

### Q: 工作流多久运行一次？
A: 每次 push 到 main 或创建标签时自动运行

### Q: 如何跳过构建？
A: 在 commit 消息中添加 `[skip ci]`
```bash
git commit -m "docs: update README [skip ci]"
```

### Q: 构建失败怎么办？
A: 查看 GitHub Actions 运行日志，检查错误信息

### Q: 可以在本地构建吗？
A: 可以，参考 `.github/WORKFLOWS_GUIDE.md` 中的本地构建指南

### Q: 如何修改工作流？
A: 编辑 `.github/workflows/*.yml` 文件，通常不需要特殊权限

## CI/CD 流程图

```
┌─ git push/tag ─┐
│                │
├─> build-all-platforms.yml
│   ├─> build-windows
│   ├─> build-macos (Intel + Apple Silicon)
│   ├─> build-linux
│   └─> create-release (仅标签)
│
└─> Artifacts & Release
    ├─ FileGather_Pro.exe (Windows)
    ├─ FileGather_Pro (macOS Intel)
    ├─ FileGather_Pro (macOS ARM64)
    └─ filegather-pro_*.deb (Linux)
```

## 关键统计

| 项目 | 值 |
|-----|-----|
| 支持平台 | 4 (Windows, macOS Intel, macOS ARM, Linux) |
| 工作流文件 | 4 个 |
| 并行构建数 | 4 (取决于 GitHub Actions 额度) |
| 平均构建时间 | ~5-10 分钟/平台 |
| Artifacts 保留期 | 30 天 |
| Release 保留期 | 永久 |

## 最佳实践

✅ **推荐**：
- 使用 `build-all-platforms.yml` 统一管理
- 标签发布时自动创建 Release
- 定期检查工作流日志
- 保持依赖版本最新

❌ **不推荐**：
- 多次修改同一个工作流
- 硬编码版本号
- 忽略构建失败
- 删除工作流文件

## 参考资源

- 📖 [GitHub Actions 文档](https://docs.github.com/en/actions)
- 📖 [.github/WORKFLOWS_GUIDE.md](.github/WORKFLOWS_GUIDE.md) - 详细工作流指南
- 📖 [PyInstaller 文档](https://pyinstaller.org/)
- 📖 [Debian 打包指南](https://www.debian.org/doc/packaging-manuals/)

---

**最后更新**: 2025-11-30  
**维护者**: ansel333
