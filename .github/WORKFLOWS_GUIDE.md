# CI/CD Build Workflows 文档

本项目使用 GitHub Actions 自动构建多平台可执行文件。

## 工作流概览

### 1. `build-all-platforms.yml` (推荐)
**统一的多平台构建工作流**

同时为所有平台构建：
- ✅ Windows 11 (Intel x64)
- ✅ macOS (Intel x86_64)
- ✅ macOS (Apple Silicon ARM64)
- ✅ Linux (Debian/Ubuntu .deb)

**触发条件**：
- `git push` 到 `main` 分支
- 标签推送 (tags: `v*`)
- 手动触发 (workflow_dispatch)

**特性**：
- 并行构建所有平台
- 完整标记时自动创建 Release
- 包含所有平台的可执行文件

### 2. `build-windows-11-intel.yml`
**专门的 Windows 构建工作流**

- 操作系统：Windows 2022
- Python 版本：3.11
- 架构：Intel x64
- 输出：`FileGather_Pro.exe`

### 3. `build-macos.yml`
**macOS 统一构建工作流（Intel & Apple Silicon）**

支持两个架构的并行构建：
- **Intel x86_64** (macOS 12)
- **Apple Silicon ARM64** (macOS 14)

输出：`FileGather_Pro`（可直接执行）

### 4. `build-linux-deb.yml`
**Linux 专用工作流（创建 .deb 包）**

- 操作系统：Ubuntu 22.04 LTS
- Python 版本：3.11
- 架构：amd64 (x86_64)
- 输出：`filegather-pro_*.deb`

## 依赖配置

### 所有平台通用
```
- PyQt6==6.7.1
- reportlab==4.4.5
- PyMuPDF==1.26.6
- python-docx==1.2.0
- openpyxl==3.1.5
- Pillow==10.4.0
- PyInstaller (最新版本)
```

### 平台特定依赖

**Windows**
- Visual C++ Build Tools (GitHub Actions 自动提供)
- Python 3.11 x64

**macOS**
- Xcode Command Line Tools (GitHub Actions 自动提供)
- Python 3.11 (universal 支持)

**Linux**
- build-essential
- python3-dev
- libqt6core6, libqt6gui6, libqt6widgets6
- fakeroot, dpkg-dev, devscripts

## 构建触发方式

### 方式 1：自动触发
```bash
# 任何 push 到 main 分支都会触发构建
git commit -m "feat: new feature"
git push origin main
```

### 方式 2：标签发布（自动创建 Release）
```bash
# 创建版本标签会自动创建 GitHub Release
git tag v2.5.0
git push origin v2.5.0
```

### 方式 3：手动触发
在 GitHub Actions 页面选择工作流，点击 "Run workflow"

## 版本自动提取

工作流使用正则表达式从 `FileGather_Pro.py` 中自动提取版本号：

```python
# 在 FileGather_Pro.py 中
class FileGatherPro(QMainWindow):
    """文件归集管理器 2.4.0"""  # <- 版本号从这里提取
```

## 构建输出

### Build Artifacts
每个工作流生成的构建产物可在 GitHub Actions 页面下载（30天保留期）

### 目录结构
```
dist/
├── FileGather_Pro.exe          # Windows 可执行文件
├── FileGather_Pro              # macOS 可执行文件
└── filegather-pro_*.deb        # Linux 安装包

output/
├── BUILD_INFO.txt              # 构建信息
└── filegather-pro_*.deb        # Linux 安装包

artifacts/
├── FileGather_Pro-Windows-11-Intel/
├── FileGather_Pro-macOS-Intel/
├── FileGather_Pro-macOS-Apple-Silicon/
└── FileGather_Pro-Linux-deb/
```

## Release 创建

**标记推送时自动创建 Release**：
```bash
git tag v2.5.0
git push origin v2.5.0
```

Release 包含：
- Windows 可执行文件
- macOS 可执行文件 (Intel & Apple Silicon)
- Linux .deb 包
- 构建信息和安装说明

## 本地构建指南

如果需要本地构建，可参考各工作流中的命令：

### Windows
```bash
pyinstaller --onefile --windowed ^
  --name FileGather_Pro ^
  --add-data "components;components" ^
  --icon app.ico ^
  --distpath dist ^
  --workpath build ^
  --clean ^
  FileGather_Pro.py
```

### macOS/Linux
```bash
pyinstaller --onefile --windowed \
  --name FileGather_Pro \
  --add-data "components:components" \
  --icon app.ico \
  --distpath dist \
  --workpath build \
  --clean \
  FileGather_Pro.py
```

## 故障排除

### 构建失败的常见原因

1. **缺少依赖**
   - 检查 `requirements.txt` 是否完整
   - 验证 PyQt6 版本兼容性

2. **图标文件缺失**
   - 可选的 `app.ico` 文件
   - 如果缺失，工作流会跳过图标集成

3. **版本提取失败**
   - 默认使用 "2.4.0"
   - 检查 `FileGather_Pro.py` 中的版本字符串格式

4. **Linux .deb 包创建失败**
   - 确保系统已安装 `fakeroot` 和 `dpkg-dev`
   - 检查目录权限

### 调试步骤

1. 查看 GitHub Actions 运行日志
2. 检查工作流文件中的具体错误信息
3. 在本地重现构建环境
4. 提交 Issue 或 PR 进行修复

## 安全性注意事项

### Code Signing (未来改进)
- Windows: 可集成 Authenticode 签名
- macOS: 可集成 Apple Developer 签名和公证
- Linux: .deb 包可使用 GPG 签名

### 依赖安全性
- 定期更新依赖包
- 使用 `--require-hashes` 验证完整性
- 监控安全公告

## 贡献指南

修改工作流时：
1. 在个人分支中测试
2. 确保所有平台都能成功构建
3. 更新此文档
4. 提交 Pull Request

## 参考资源

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [PyInstaller 文档](https://pyinstaller.org/en/stable/)
- [Debian 打包指南](https://www.debian.org/doc/manuals/debian-faq/ch-pkg_basics.en.html)
- [macOS 可执行文件指南](https://developer.apple.com/documentation/macos-release-notes)

---

**最后更新**: 2025-11-30  
**维护者**: ansel333
