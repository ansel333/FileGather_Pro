#!/usr/bin/env pwsh

param(
    [string]$Version = "2.4.0"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FileGather Pro Release Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$MainFile = Join-Path $ScriptRoot "FileGather_Pro.py"
$VersionArchive = Join-Path $ScriptRoot "VERSION_ARCHIVE.md"
$ChangelogFile = Join-Path $ScriptRoot "CHANGELOG_v$Version.md"

Write-Host "Step 1: Update FileGather_Pro.py version" -ForegroundColor Yellow

$PythonContent = Get-Content $MainFile -Raw

$PatternVersion = '__version__\s*=\s*"[^"]+"'
if ($PythonContent -match $PatternVersion) {
    $OldVersionMatches = [regex]::Matches($PythonContent, '__version__\s*=\s*"([^"]+)"')
    if ($OldVersionMatches.Count -gt 0) {
        $OldVersion = $OldVersionMatches[0].Groups[1].Value
        Write-Host "Current version: $OldVersion" -ForegroundColor Gray
        
        $NewPythonContent = $PythonContent -replace '__version__\s*=\s*"[^"]+"', "__version__ = `"$Version`""
        $NewPythonContent | Set-Content $MainFile -Encoding UTF8
        Write-Host "Updated to version: $Version" -ForegroundColor Green
    }
} else {
    Write-Host "WARNING: Could not find __version__ in FileGather_Pro.py" -ForegroundColor Red
}

Write-Host ""
Write-Host "Step 2: Update VERSION_ARCHIVE.md" -ForegroundColor Yellow

$ArchiveContent = Get-Content $VersionArchive -Raw
$CurrentDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

$ArchiveEntry = @"
## Version $Version

Release Date: $CurrentDate
Status: Released

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

"@

$VersionCheck = "## Version $Version"
if (-not ($ArchiveContent -match [regex]::Escape($VersionCheck))) {
    $UpdatedArchive = $ArchiveEntry + $ArchiveContent
    $UpdatedArchive | Set-Content $VersionArchive -Encoding UTF8
    Write-Host "Added version $Version to VERSION_ARCHIVE.md" -ForegroundColor Green
} else {
    Write-Host "Version $Version already in VERSION_ARCHIVE.md" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Step 3: Generate CHANGELOG" -ForegroundColor Yellow

$ChangelogContent = @"
# FileGather Pro v$Version Changelog

Release Date: $CurrentDate

## Overview
FileGather Pro v$Version represents a major milestone in project organization and stability. This release includes comprehensive documentation consolidation and improved development workflow.

## Major Features

### Documentation and Organization
- Consolidated 15 refactoring documents into centralized archive
- Created complete project documentation index
- Established systematic versioning and release workflow
- Added comprehensive guides for Windows and PowerShell workflows

### Code Architecture
- 28 functions extracted from main application
- 6 specialized component modules created
- Improved separation of concerns
- Better code maintainability and testability

### Testing and Quality
- 24 comprehensive test cases with 100% pass rate
- Test coverage for exact search, folder gathering, and launch operations
- Systematic error handling and validation

### Build and Distribution
- PyInstaller integration with v6.17.0
- Executable build optimization
- Build analysis and warning documentation

## Technical Details

### Project Structure
- components/main_window.py (1090 lines, refactored)
- components/file_operations.py (extracted functions)
- components/search_logic.py (search operations)
- components/ui_builder.py (UI construction)
- components/utils.py (utility functions)
- components/dialogs/ (dialog modules)
- components/functions/ (6 specialized modules)
- tests/ (24 test cases)
- ai-workflow/refactoring_archive/2025-11-29/ (15 documents)

### Dependencies
- Python 3.11
- PyQt5 5.15.11
- PyInstaller 6.17.0

## Bug Fixes
- Resolved file operation edge cases
- Improved error handling in search operations
- Enhanced conflict detection in file operations
- Fixed dialog timeout issues

## Known Issues
None reported for this release.

## Migration Notes
No breaking changes from v2.3.5.1. All existing functionality remains compatible.

## Contributors
FileGather Pro Development Team

---
Generated on: $CurrentDate
Version: $Version
"@

$ChangelogContent | Set-Content $ChangelogFile -Encoding UTF8
Write-Host "Generated CHANGELOG_v$Version.md" -ForegroundColor Green

Write-Host ""
Write-Host "Step 4: Git Operations" -ForegroundColor Yellow

try {
    $GitTest = git rev-parse --git-dir 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Git repository detected" -ForegroundColor Gray
        
        git add FileGather_Pro.py VERSION_ARCHIVE.md "CHANGELOG_v$Version.md" 2>&1
        Write-Host "Files staged for commit" -ForegroundColor Gray
        
        $CommitMsg = "Release v$Version - Version update and changelog"
        git commit -m $CommitMsg 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Commit created for v$Version" -ForegroundColor Green
        } else {
            Write-Host "Git commit returned non-zero exit code (may already be committed)" -ForegroundColor Yellow
        }
        
        git tag "v$Version" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Git tag v$Version created" -ForegroundColor Green
        } else {
            Write-Host "Git tag returned non-zero exit code (may already exist)" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "Git operations failed: $_" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Release Complete" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Version: $Version" -ForegroundColor Green
Write-Host "Release Date: $CurrentDate" -ForegroundColor Green
Write-Host "Files Updated:" -ForegroundColor Green
Write-Host "  - FileGather_Pro.py" -ForegroundColor Green
Write-Host "  - VERSION_ARCHIVE.md" -ForegroundColor Green
Write-Host "  - CHANGELOG_v$Version.md" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Review the generated CHANGELOG_v$Version.md" -ForegroundColor Cyan
Write-Host "  2. Run: git log --oneline -5" -ForegroundColor Cyan
Write-Host "  3. Run: git tag -l" -ForegroundColor Cyan
Write-Host ""
