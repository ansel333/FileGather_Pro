# FileGather Pro Version Archive

## Version 2.5.1 (2025-12-01)

**Release Date**: 2025-12-01  
**Status**: Released  
**Branch**: main

### Major Features

- ✅ **UI Improvements & Bug Fixes**
  - Added reset button to restore application to initial state
  - Improved unfound keywords display with tree widget
  - Added copy feedback labels for user interaction
  - Fixed keyword statistics to display all found keywords
  - Single-result keywords now displayed in separate tree widget
  
- ✅ **Enhanced Search Experience**
  - Support for consecutive searches (fuzzy → exact or vice versa)
  - Better button state management during search operations
  - Improved layout spacing when unfound keywords are present

- ✅ **User Experience**
  - Reset button clears all data and resets window size to initial state
  - Copy operations show feedback with keyword count
  - Better visual hierarchy for search results

### Bug Fixes

- Fixed issue where consecutive searches (exact then fuzzy or vice versa) would fail
- Fixed unfound keywords not displaying correctly
- Fixed button layout alignment issues
- Improved tree widget visibility control

### Technical Improvements

- Refactored keyword display logic
- Better state management for search operations
- Improved UI component initialization

---

## Version 2.5.0 (2025-11-30)

**Release Date**: 2025-11-30  
**Status**: Released  
**Branch**: main

### Major Features

- 🎯 **Folder Gathering Mode**: Collect entire folder hierarchies instead of individual files
  - New `gather_mode_combo` dropdown: File Collection / Folder Collection
  - `_start_folder_search()`: Fuzzy matching on folder names
  - `_start_folder_exact_search()`: Exact matching on folder names
  - Searches only the **first level** subfolders of target directory
  - Auto-hides file type filters and subfolder recursion options in folder mode

- 🎨 **UI Improvements**:
  - Gather mode selector visible in search conditions row
  - Hidden "File Type" and "Include Subfolders" options in folder mode
  - Status bar shows "Found X folders" (not file count)

### Code Changes

- `components/ui_builder.py`:
  - New `gather_mode_combo` component
  - Created `subfolders_container` widget container for visibility control
  - Return tuple expanded to 17 elements

- `components/main_window.py`:
  - Implemented `on_gather_mode_changed()` method for mode switching
  - Implemented `_start_folder_search()` method
  - Implemented `_start_folder_exact_search()` method
  - `start_search()` and `start_exact_search()` route to folder search methods

### Feature Comparison

| Feature | File Collection | Folder Collection |
|---------|-----------------|-------------------|
| Search Target | Individual files | Directory subfolders |
| Search Scope | Recursive to all subdirs | First level only |
| File Type Filter | ✅ Supported | ✅ Not applicable |
| Subfolder Recursion | ✅ Optional | ✅ Disabled |
| Exact/Fuzzy Matching | ✅ Both | ✅ Both |
| Search Pattern | By filename/content/hybrid | Folder names only |

---

## Version 2.4.0 (2025-11-29)

**Release Date**: 2025-11-29 23:08:18  
**Status**: Released

### Key Features
- Enhanced modular architecture with 28 extracted functions
- Improved dialog system with conflict handling
- Advanced search functionality with zero-result keywords
- Better file operations with error handling
- Comprehensive documentation and testing

### Files Consolidated
- Moved 15 refactoring documents to ai-workflow/refactoring_archive/2025-11-29/
- Total documentation: 105.5 KB
- Complete project restructuring documented

### Technical Improvements
- Code modularization completed across 6 component modules
- Extended test suite with 24 test cases
- Build optimization with PyInstaller 6.17.0
- Windows and PowerShell workflow documentation

---

## Version 2.3.5.1 (2025-11-29)

**Release Date**: 2025-11-29 21:54:51  
**Tag**: `2.3.5.1`  
**Branch**: main

### Major Commits

| Commit Hash | Message | Date |
|-------------|---------|------|
| `7126642` | fix: correct delete button label for accuracy | 2025-11-29 |
| `c2d885b` | feat: add exact filename matching search mode and improve UI layout | 2025-11-29 |
| `5adc9a8` | docs: add ansel333 as co-author and contributor | 2025-11-29 |
| `304964a` | ci: configure workflow to upload exe to GitHub release | 2025-11-29 |

### New Features

- ✅ **Exact Search Mode**: Support exact filename matching
  - New `exact_match_filename()` function
  - Added `start_exact_search()` method
  - Exact filename matching (ignoring extensions)

- 🔧 **UI Optimization**: Buttons reorganized into three-row layout
  - Row 1: 🔍 Fuzzy Search | ✅ Exact Search | ⏸️ Cancel Search
  - Row 2: 📂 Select Target | 🔄 Start Gathering | 🗑️ Delete Original Files
  - Row 3: 📋 Generate Log | ⚙️ Usage Instructions
  - Added tooltips to all buttons

- 📚 **Documentation Complete**: Launch scripts and guides
  - `run.ps1`: PowerShell quick launch script
  - `run.bat`: Batch quick launch script
  - `LAUNCH_GUIDE.md`: Complete launch guide

### Technical Changes

- Code file refactoring:
  - `search_logic.py`: Added exact matching logic
  - `ui_builder.py`: Optimized button layout (3-tuple return values)
  - `main_window.py`: Handle exact search functionality

- Build tools:
  - `.gitignore`: Added `build_2.3.4/` ignore rule
  - `build_2.3.4/`: Build directory for v2.3.4 comparison

### Executable Files

| Filename | Size | Release Date |
|----------|------|-------------|
| FileGather_Pro.exe | 70.59 MB | 2025-11-29 21:10:52 |
| FileGather_Pro_2.3.4.exe | 70.44 MB | 2025-11-29 21:54:51 |

### File Cleanup

- Renamed `FileGather_Pro2.3.5.py` → `FileGather_Pro.py`
- Reason: Version is managed by code, no need to duplicate in filename

---

## Version 2.3.5 (2025-11-29)

**Release Date**: 2025-11-29 13:00:00  
**Tag**: `2.3.5`  
**Branch**: main  
**First Commit**: `9448e0b`

### Major Commits

| Commit Hash | Message | Date |
|-------------|---------|------|
| `9448e0b` | refactor: organize AI workflow documentation and finalize v2.3.5 | 2025-11-29 |

### Major Achievements

- ✅ **Complete Modularization**: 1686-line single file → modular structure
  - `main_window.py`: Main window and search logic (832 lines)
  - `ui_builder.py`: UI component factory (444 lines)
  - `search_logic.py`: Search algorithms (121 lines)
  - `file_operations.py`: File operations (130 lines)
  - `utils.py`: Utility functions (100 lines)
  - `dialogs/`: Dialog boxes package (3 specialized modules)

- 📦 **Dialogs Package Refinement**
  - `search_result_dialog.py`
  - `conflict_dialog.py`
  - `pdf_generator.py`

- 📋 **Project Organization**
  - AI workflow docs moved to `ai-workflow/`
  - Created `archive/` folder for archived versions
  - Added `.gitignore` configuration
  - Complete documentation structure

### Executable Files

| Filename | Size | Release Date |
|----------|------|-------------|
| FileGather_Pro.exe | 67.32 MB | 2025-11-29 13:00:00 |

---

## Version 2.3.4 (2025-07-17)

**Tag**: `2.3.4`  
**Branch**: main  
**Status**: Archived

### Features

- Single file structure (1686 lines)
- Multi-format file support (TXT, PDF, DOCX, XLSX)
- Advanced keyword matching
- Fuzzy search functionality
- PDF report generation

### Executable Files

| Filename | Size |
|----------|------|
| FileGather_Pro_2.3.4.exe | 70.44 MB |

---

## Version Comparison Summary

| Feature | v2.3.4 | v2.3.5 | v2.3.5.1 | v2.4.0 | v2.5.0 | v2.5.1 |
|---------|--------|--------|----------|--------|--------|--------|
| Code Structure | Single file, 1686 lines | Modular, 6 modules | Modular, 6 modules | Modular, enhanced | Modular, folder mode | Modular, enhanced |
| Exact Search | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Fuzzy Search | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Advanced Keywords | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Reset Button | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Tree Widget Keywords | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Button Layout | Single row | Single row | Three rows | Optimized | Optimized | Optimized |
| Tool Tooltips | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Quick Launch Scripts | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| CI/CD Automation | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Folder Collection | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Code Maintainability | Low | High | High | High | High | High |

---

## Release Workflow

For each new version:

1. **Code Development**: Complete all feature development and testing
2. **Documentation Update**: 
   - Update `README.md` version and features
   - Update this file (VERSION_ARCHIVE.md) with version info
3. **Create Tag**:
   ```bash
   git tag -a X.X.X -m "Release vX.X.X - Feature description"
   git push origin X.X.X
   ```
4. **Create Release**:
   - GitHub Release auto-attaches executable
   - Include version notes and changelog
5. **Update Version Archive**: Add entry to this file

---

**Last Updated**: 2025-12-01  
**Maintainers**: daiyixr, ansel333  
**Repository**: https://github.com/ansel333/FileGather_Pro
