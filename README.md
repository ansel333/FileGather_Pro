# FileGather Pro

> 💼 Professional File Collection and Search Management Tool

A powerful file management tool for quickly searching, categorizing, and managing large volumes of documents. Supports multi-format file search, advanced keyword matching, conflict handling, and PDF report generation.

**Current Version**: v2.5.1 (2025-12-01)

📖 **Available in other languages**: [中文 (Chinese)](README.zh-CN.md)

---

## ✨ Key Features

### 🔍 Advanced Search
- **Two search modes**:
  - **Fuzzy Search** (default): Search for files containing keywords in filename
  - **Exact Search**: Search for files with exact filename match
- **Advanced keyword syntax**: `+keyword`, `-keyword`, `|`, `*`, `"exact phrase"`
- **Multi-format support**: TXT, PDF, DOCX, XLSX

### 📁 File Management
- Add/remove search folders
- Support local disk and network paths
- Batch copy and delete files
- Smart conflict handling (overwrite, skip, rename)

### 📊 Report Generation
- Generate PDF operation logs
- Include search criteria, operation records, file lists
- Support exporting selected records (first 20, first 50, all)
- Chinese font support

### 🎨 User Interface
- Modern PyQt6 interface (6.7.1)
- White background + colored border button design
- Single-line compact button layout
- Real-time search result preview
- Right-click context menu
- Progress indication and status feedback
- Conditional visibility cancel button

---

## 🚀 Quick Start

### Run the Program
```bash
python FileGather_Pro.py
```

### Or Use Executable File
```bash
FileGather_Pro.exe  # Windows executable (includes custom icon)
```

### Basic Usage Flow
1. **Start the program**: Run the main program file to launch the application
2. **Add search folders**: Click "Add Folder" button to select directories to search
3. **Enter search criteria**: Input keywords or filename
4. **Choose search type**:
   - 🔍 **Fuzzy Search**: Search for files containing keywords (supports advanced syntax)
   - ✓ **Exact Search**: Search for files with exact filename match
5. **Start search**: Click the corresponding search button
6. **View results**: Search results display in the table below
7. **Handle files**: Right-click or use buttons for copy, delete, and other operations
8. **Generate report**: Click "Generate PDF Log" to export operation records

---

## 🧪 Testing

### Installation
```bash
# Install test dependencies
pip install -r requirements-test.txt
```

### Running Tests
```bash
# Run all tests (47+ tests passing)
$env:QT_QPA_PLATFORM='offscreen'
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/test_file_operations.py -v    # File/folder operations (11 tests)
python -m pytest tests/test_pyqt6_dialogs.py -v      # PyQt6 enum handling (12 tests)
python -m pytest tests/test_gather_mode_routing.py -v # Gather mode routing (14 tests)
python -m pytest tests/test_search_logic.py -v       # Search logic (20 tests)

# Run with coverage report
python -m pytest tests/ --cov=components --cov-report=html

# Run only unit tests
python -m pytest tests/ -m unit -v

# Using the test runner script
python run_tests.py all           # Run all tests
python run_tests.py unit          # Run unit tests only
python run_tests.py coverage      # Generate coverage report
python run_tests.py list          # List all available tests
```

### Test Coverage
- **11 tests** in `test_file_operations.py` - File/folder copy, delete, batch operations, hash calculation
- **12 tests** in `test_pyqt6_dialogs.py` - PyQt6 enum handling, dialog return values, button combinations
- **14 tests** in `test_gather_mode_routing.py` - File vs folder mode routing, conditional logic, operations
- **20 tests** in `test_search_logic.py` - Exact match, keyword matching, content search
- **47+ total tests** passing with comprehensive coverage
- Environment: Python 3.11.9, pytest 7.4.3, PyQt6 6.7.1

---

## 📦 Project Structure

### v2.4.0 Architecture (Modular + Feature Extension + Automated Build)

```
FileGather_Pro/
├── FileGather_Pro.py                # Application entry point (v2.5.1)
├── FileGather_Pro.spec              # PyInstaller configuration
├── app.ico                          # Application icon (256×256)
├── components/                      # Core modules package
│   ├── __init__.py
│   ├── main_window.py               # Main window class (167 lines, -85%)
│   ├── ui_builder.py                # UI builder
│   ├── search_logic.py              # Search logic
│   ├── file_operations.py           # File operations
│   ├── utils.py                     # Utility functions
│   ├── dialogs/                     # Dialogs sub-package
│   │   ├── __init__.py
│   │   ├── search_result_dialog.py  # Search result dialog
│   │   ├── conflict_dialog.py       # Conflict handling dialog
│   │   ├── pdf_generator.py         # PDF generator
│   │   └── README.md
│   ├── functions/                   # Business logic modules (28+ functions)
│   │   ├── __init__.py
│   │   ├── folder_manager.py        # Folder management
│   │   ├── search_manager.py        # Search management
│   │   ├── results_manager.py       # Results management
│   │   ├── search_operations.py     # Search operations
│   │   ├── file_operations_ui.py    # UI file operations
│   │   ├── ui_interactions.py       # UI interactions
│   │   └── README.md
│   └── README.md
├── tests/                           # Test suite (47+ tests)
├── archive/                         # Old version archives
├── ai-workflow/                     # Workflow documentation
├── .github/workflows/               # GitHub Actions CI/CD
│   └── build-all-platforms.yml      # Multi-platform automated build
├── .gitignore                       # Git ignore configuration
├── LICENSE                          # Apache 2.0 license
└── README.md                        # Project documentation
```

### Architecture Features
- ✅ **Single Responsibility Principle** - Each module focuses on one function
- ✅ **Low Coupling** - Modules are independent and easy to test
- ✅ **High Cohesion** - Related functionality concentrated in same module
- ✅ **Easy Extension** - Add new features by creating new modules
- ✅ **85% Code Reduction** - Main window reduced from 1090 to 167 lines
- ✅ **Professional Icon** - 256×256 multi-resolution icon integration
- ✅ **Automated Build** - GitHub Actions CI/CD workflow
- ✅ **Complete Tests** - 47+ test cases all passing

---

## 🔧 Dependencies

| Package | Purpose |
|---------|---------|
| **PyQt6** | GUI framework (6.7.1) |
| **reportlab** | PDF generation |
| **PyMuPDF** | PDF content extraction |
| **python-docx** | Word file processing |
| **openpyxl** | Excel file processing |
| **Pillow** | Image processing and icon generation |

### Install Dependencies
```bash
pip install PyQt6==6.7.1 reportlab==4.4.5 PyMuPDF==1.26.6 python-docx==1.2.0 openpyxl==3.1.5 Pillow==10.4.0
```

### Run from Executable File (Recommended)
```bash
# No dependencies needed, run directly
./FileGather_Pro.exe
```

---

## 🚨 Important Notes

### Performance Recommendations
- Large-scale search: Filter by filename first
- Content search: More time-consuming than filename search, please be patient
- Network paths: May be slower, recommend mapping to local drive first

### Security Tips
- ⚠️ Delete operations are **irreversible**, please confirm before executing
- ⚠️ Only use for legitimate file management operations
- ⚠️ Avoid improper operations on system files or protected files
- ⚠️ Regular backup of important files recommended

---

## 📚 Documentation

- **REFACTORING.md** - Detailed refactoring and architecture design
- **DIALOGS_REFACTORING.md** - Dialog package splitting documentation
- **QUICK_REFERENCE.md** - Quick reference guide
- **.github/WORKFLOWS_GUIDE.md** - Detailed CI/CD workflow guide
- **.github/BUILD_GUIDE.md** - Multi-platform build quick reference
- **components/README.md** - Module structure documentation
- **components/dialogs/README.md** - Dialogs package documentation

---

## 📝 Version History

### 🎉 v2.5.0 (2025-11-30) - Unified Version Management & Multi-Platform Release
**Major Improvements**:
- 🔄 **Unified Version Source**
  - Created `VERSION` file as the single source of truth
  - All code and workflows read version from `VERSION` file
  - No need to modify multiple files, improving maintenance efficiency
  
- 🚀 **Multi-Platform CI/CD Optimization**
  - All workflows updated to read version from `VERSION` file
  - Support 4 build platforms: Windows 11, macOS Intel, macOS ARM64, Linux .deb
  - Workflows automatically create GitHub Release
  - Tag push automatically triggers parallel builds
  
- 📋 **Project Documentation Enhancement**
  - Added `PROJECT_NAVIGATION.md` - Project navigation guide
  - Added `PROJECT_COMPLETION_REPORT.md` - Complete project report
  - Added `CLEANUP_SUMMARY.md` - Cleanup summary document
  - All documentation updated to latest version
  
- 🧹 **Project Cleanup**
  - Removed duplicate specialized workflows (consolidated to build-all-platforms.yml)
  - Removed obsolete workflow configurations
  - All outdated files cleaned up

**Technical Details**:
- VERSION file: Centralized version management
- main_window.py: Dynamic version reading
- Workflows: Changed to extract version from VERSION file
- 47+ unit tests all passing
- 1 unified GitHub Actions workflow

### 🎉 v2.4.0 (2025-11-29) - Main Window Simplification & Icon Integration & PyQt6 Upgrade
**Major Improvements**:
- 🔧 **Main Window Refactoring**: Code reduced from 1090 to 167 lines (-85%)
  - Removed 29 duplicate methods
  - Extracted all business logic to functions/ module
  - Retained 5 core framework methods
  
- 🎨 **Professional Icon Integration**
  - Integrated 256×256 multi-resolution application icon
  - Perfect display in File Explorer, Start Menu, Taskbar
  - PyInstaller automatically embeds icon in executable
  
- 🔧 **PyQt6 Upgrade**
  - Upgraded framework from PyQt5 5.15.11 to PyQt6 6.7.1
  - Fixed 20+ PyQt6 enum constants (AlignmentFlag, ItemDataRole, SelectionMode, etc.)
  - Updated dialog exec() calls and StandardButton enums
  - Optimized button styles: white background + colored border + hover effects
  - Added conditional visibility cancel button (visible during search)
  
- 📝 **Enhanced Test Coverage**
  - Added 11 file/folder operation tests
  - Added 12 PyQt6 enum handling tests
  - Added 14 gather_mode routing tests
  - Total 47+ unit tests, all passing
  - Verified folder copy/delete functionality
  - Verified conditional routing logic
  
- 🔄 **Multi-Platform Build Optimization**
  - Windows 11 (Intel x64) automated build
  - macOS Intel x86_64 and Apple Silicon ARM64 parallel builds
  - Linux creates .deb installation package
  - Automatic GitHub Release creation on tag push
  
- 📦 **Project Cleanup**
  - Removed temporary build files and scripts
  - Retained only production-necessary core files
  - Workspace streamlined

**Technical Details**:
- components/main_window.py: 167 lines (framework code)
- components/functions/: 28+ business logic functions
- PyQt6 6.7.1 framework upgrade (from 5.15.11)
- 47+ unit tests, comprehensive coverage
- PyInstaller v6.17.0 configuration
- GitHub Actions multi-platform automated build

### ✨ v2.3.5.1 (2025-11-29) - Exact Search Feature
**New Features**:
- 🎯 **Exact Search Mode**
  - New "✓ Exact Search" button supporting strict filename matching
  - Exact search ignores file extensions, matches only filename body
  - Example: Keyword "report" only matches "report.xlsx", "report.pdf", etc., not "annual_report.docx"

- 🎨 **UI Optimization**
  - Rearranged buttons to three-row layout, more intuitive
  - Row 1: 🔍 Fuzzy Search | ✓ Exact Search | ⏹ Cancel Search
  - Row 2: 📂 Select Target | 📋 Start Gather | 🗑 Delete Original
  - Row 3: 📄 Generate Log | ❓ Instructions
  - Added tooltips explaining button functions

- 🔍 **Search Logic Improvements**
  - Added `exact_match_filename()` function in `search_logic.py`
  - Exact search uses dedicated matching logic, no advanced syntax support (basic keywords only)
  - Fuzzy search retains all advanced features (AND/OR logic, exclusion, wildcards, etc.)

**Technical Improvements**:
- Split search logic: `start_search()` handles fuzzy search, `start_exact_search()` handles exact search
- Code reuse: Shared file traversal, size/date filtering logic

### 🎯 v2.3.5 (2025-11-29) - Complete Modular Refactoring
**Main Improvements**:
- ✨ **Architecture Refactoring**: 1686-line single file → modular structure
  - Average file size 340 lines, easier to maintain
  - Single responsibility principle, clear module boundaries
  
- 📦 **Dialogs Package Refinement**: Split into multiple professional modules
  - `search_result_dialog.py` - Search result display (60 lines)
  - `conflict_dialog.py` - Conflict handling (200 lines)
  - `pdf_generator.py` - PDF report generation (210 lines)
  
- 📚 **Documentation Enhancement**:
  - REFACTORING.md - Detailed refactoring explanation
  - DIALOGS_REFACTORING.md - Dialog split report
  - components/README.md - Module structure explanation
  - QUICK_REFERENCE.md - Quick reference guide
  
- 🏗️ **Project Organization**:
  - Created archive folder for old versions
  - Added .gitignore file (supports Python, IDE, build artifacts)
  - Cleaned up build/ and dist/ directories

### v2.3.4 (2025-07-17)
- Optimized search results and button display
- Updated application icon to app.ico
- Fixed icon display issues

### v2.3.3
- Multi-language support, PDF, Word and Excel file search (deprecated)

---

## 🎯 Use Cases

- **Document Management**: Quickly locate company documents and reports
- **Code Search**: Search for specific code snippets in large projects
- **Log Analysis**: Find and analyze information in log files
- **Content Filtering**: Extract files meeting conditions from large volumes
- **File Organization**: Batch copy and organize files

---

## 📄 License

This project is licensed under the **Apache 2.0** License.  
See the [LICENSE](LICENSE) file for details.

---

## 📦 Getting Executable Files

### Multi-Platform Support
FileGather Pro now supports automated builds for the following platforms:
- ✅ **Windows 11** (Intel x64)
- ✅ **macOS** (Intel x86_64 and Apple Silicon ARM64)
- ✅ **Linux** (Ubuntu/Debian .deb package)

### Download from GitHub Release
Visit [Releases](https://github.com/ansel333/FileGather_Pro/releases) page to download the latest version of executable files

**v2.4.0+ Features**:
- ✅ Cross-platform support (Windows, macOS, Linux)
- ✅ Includes custom application icon
- ✅ Optimized code structure (-85% code)
- ✅ Complete feature set
- ✅ No Python environment required

#### Windows
Simply run `FileGather_Pro.exe`

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

## 👤 Author and Contributors

**Project Name**: FileGather Pro  
**Developer**: [daiyixr](https://github.com/daiyixr)  
**Contributors**: [ansel333](https://github.com/ansel333) - Code refactoring, UI optimization, CI/CD workflows, icon integration  
**Created**: 2024  
**Last Updated**: 2025-11-30  

---

## 📞 Feedback and Support

If you have questions or suggestions, please:
- Submit an Issue
- Create a Pull Request
- Contact the developers

---

## 📖 Project Origin

**FileGather Pro** originated as a fork of [daiyixr/FileGather](https://github.com/daiyixr/FileGather) but has since evolved into an independent project with significant changes:

- ✅ Complete architectural refactoring (1686 lines → modular structure)
- ✅ Upgraded from PyQt5 to PyQt6 6.7.1
- ✅ Comprehensive multi-platform CI/CD workflows (Windows, macOS, Linux)
- ✅ 47+ unit tests with full test coverage
- ✅ Unified version management system
- ✅ Professional icon integration and UI optimization
- ✅ Enhanced documentation and project organization

**Note**: Due to substantial changes and divergence from the original project, merging back is no longer feasible. This repository maintains its own independent development path.

---

## 🙏 Acknowledgments

**Special thanks to:**
- [daiyixr](https://github.com/daiyixr) - Original FileGather project creator

**Open-source projects used:**
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - GUI framework (6.7.1)
- [PyInstaller](https://www.pyinstaller.org/) - Executable file building
- [ReportLab](https://www.reportlab.com/) - PDF generation
- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF processing
- [python-docx](https://python-docx.readthedocs.io/) - Word processing
- [openpyxl](https://openpyxl.readthedocs.io/) - Excel processing
- [Pillow](https://python-pillow.org/) - Image processing

---

**Made with ❤️ for efficient file management**

