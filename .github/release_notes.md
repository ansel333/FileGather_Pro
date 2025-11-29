## 📦 FileGather Pro v2.3.5 Release

### ✨ What's New

#### Code Refactoring
- Modularized monolithic codebase into 9 focused components
- Improved code organization with single responsibility principle
- Enhanced maintainability and testability

#### UI Optimization
- Integrated keyword search results into main results table
- Added dedicated unfound keywords display area (red-themed)
- Implemented dynamic view buttons for multi-result keywords
- Optimized keyword statistics display (hidden single-result keywords)

#### New Features
- Keyword statistics showing 0-result and multiple-result keywords
- Blue "View" buttons for keywords with multiple matches
- Copyable unfound keywords list (one per line)
- Production-ready Windows executable (.exe file)

#### CI/CD Automation
- GitHub Actions workflows for Windows 11 (x64)
- GitHub Actions workflows for macOS (Intel)
- Automated executable packaging with PyInstaller
- Cross-platform build automation

### 🔧 Technical Details

**Technology Stack:**
- Python 3.11
- PyQt5 5.15.11
- PyInstaller 6.17.0
- ReportLab 4.4.5 (PDF generation)
- PyMuPDF 1.26.6 (PDF processing)
- python-docx 1.2.0 (Word files)
- openpyxl 3.1.5 (Excel files)
- Pillow 10.4.0 (Image processing)

**Architecture:**
- Modular component-based design
- Factory Pattern for UI creation
- Dedicated dialogs sub-package
- Comprehensive error handling

### 📥 Installation

1. Download `FileGather_Pro.exe` from the assets below
2. Run the executable (no installation required)
3. Or clone and run: `python FileGather_Pro2.3.5.py`

### 👥 Contributors

- **daiyixr** - Original author
- **ansel333** - Code refactoring, UI optimization, CI/CD workflows

### 📝 Notes

This is a production-ready release with:
- Comprehensive testing on Windows 11
- Cross-platform CI/CD support
- Well-documented codebase
- Professional-grade code organization

---

**Build Date:** Automated via GitHub Actions  
**Platform:** Windows 11 (Intel/x64) | macOS (Intel)
