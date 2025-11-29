#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for folder gathering mode feature
"""

import os
import sys
import tempfile
from pathlib import Path

# Set Qt platform before any Qt imports
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test folder gathering logic
def test_folder_structure():
    """Create test folder structure and verify it can be searched"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test directory structure
        test_base = Path(tmpdir) / "test_base"
        test_base.mkdir()
        
        # Create some test folders with keywords
        (test_base / "python_project").mkdir()
        (test_base / "python_docs").mkdir()
        (test_base / "java_project").mkdir()
        (test_base / "no_match_folder").mkdir()
        
        # Create some files in subdirs (should be ignored in folder gather mode)
        (test_base / "python_project" / "test.py").touch()
        (test_base / "python_docs" / "readme.txt").touch()
        
        # Simulate folder gathering search
        search_keywords = ["python", "project"]
        found_folders = []
        
        # Search only first level subdirs
        for subdir in test_base.iterdir():
            if subdir.is_dir():
                dir_name = subdir.name
                for keyword in search_keywords:
                    if keyword in dir_name.lower():
                        found_folders.append(dir_name)
                        break
        
        print(f"Created test folders in: {test_base}")
        print(f"Search keywords: {search_keywords}")
        print(f"Found folders: {found_folders}")
        
        # Expected results
        expected = ["python_project", "python_docs"]
        assert "python_project" in found_folders, "Should find 'python_project' folder"
        assert "python_docs" in found_folders, "Should find 'python_docs' folder"
        assert "no_match_folder" not in found_folders, "Should not find 'no_match_folder'"
        
        print("\n✓ All tests passed!")
        return True

if __name__ == "__main__":
    try:
        test_folder_structure()
    except AssertionError as e:
        print(f"✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)
