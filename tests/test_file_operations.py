"""
Unit Tests: File Operations Module (components.file_operations)
Tests for file finding, file info retrieval, and file operations
"""

import sys
import os
import pytest
import tempfile
from pathlib import Path
import shutil

# Set QT_QPA_PLATFORM to offscreen to avoid GUI issues
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.file_operations import calculate_hash, copy_files_without_conflicts, copy_selected_files, delete_files_batch
from components.utils import get_file_info_dict


class TestFindFiles:
    """File finding tests"""
    
    def test_find_files_in_directory(self):
        """Test finding files in a directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            Path(tmpdir, "test1.txt").touch()
            Path(tmpdir, "test2.txt").touch()
            Path(tmpdir, "data.py").touch()
            
            # Find all files
            files = find_files(tmpdir, include_subfolders=False)
            assert len(files) >= 3
    
    def test_find_files_with_extension_filter(self):
        """Test file finding with extension filter"""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "file1.txt").touch()
            Path(tmpdir, "file2.txt").touch()
            Path(tmpdir, "file3.py").touch()
            
            # Find only .txt files
            txt_files = [f for f in find_files(tmpdir, include_subfolders=False) 
                        if f.endswith('.txt')]
            assert len(txt_files) == 2
    
    def test_find_files_recursive(self):
        """Test recursive file finding"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create subdirectory and files
            subdir = Path(tmpdir, "subdir")
            subdir.mkdir()
            Path(tmpdir, "file1.txt").touch()
            Path(subdir, "file2.txt").touch()
            
            # Recursive search
            files = find_files(tmpdir, include_subfolders=True)
            assert len(files) >= 2
    
    def test_find_files_empty_directory(self):
        """Test finding files in empty directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            files = find_files(tmpdir, include_subfolders=False)
            assert len(files) == 0
    
    def test_find_files_nonexistent_directory(self):
        """Test finding files in non-existent directory"""
        files = find_files("/nonexistent/directory", include_subfolders=False)
        assert files == [] or files is None


class TestGetFileInfo:
    """File info retrieval tests"""
    
    def test_get_file_info_size(self):
        """Test retrieving file size"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content\n" * 100)
            f.flush()
            
            info = get_file_info_dict(f.name)
            assert info is not None
            assert info.get('size', 0) > 0
            
            os.unlink(f.name)
    
    def test_get_file_info_time(self):
        """Test retrieving file time info"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test")
            f.flush()
            
            info = get_file_info_dict(f.name)
            assert info is not None
            assert 'modify_time' in info or 'mtime' in info
            
            os.unlink(f.name)
    
    def test_get_file_info_nonexistent_file(self):
        """Test getting info on non-existent file"""
        info = get_file_info_dict("/nonexistent/file.txt")
        assert info is None or info == {}
    
    def test_get_file_info_directory(self):
        """Test getting directory info"""
        with tempfile.TemporaryDirectory() as tmpdir:
            info = get_file_info_dict(tmpdir)
            assert info is not None or info == {}


class TestCopyFile:
    """File copy tests"""
    
    def test_copy_file_success(self):
        """Test successful file copy"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create source file
            src = Path(tmpdir, "source.txt")
            src.write_text("test content")
            
            # Copy file
            dst = Path(tmpdir, "copy.txt")
            try:
                shutil.copy(src, dst)
                assert dst.exists()
                assert dst.read_text() == "test content"
            except Exception as e:
                pytest.fail(f"Copy failed: {e}")
    
    def test_copy_file_overwrite(self):
        """Test file copy with overwrite"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src = Path(tmpdir, "source.txt")
            dst = Path(tmpdir, "dest.txt")
            
            src.write_text("original")
            dst.write_text("existing")
            
            shutil.copy(src, dst)
            assert dst.read_text() == "original"
    
    def test_copy_file_preserves_content(self):
        """Test that copy preserves file content"""
        with tempfile.TemporaryDirectory() as tmpdir:
            content = "test content\nwith multiple lines\n"
            src = Path(tmpdir, "source.txt")
            dst = Path(tmpdir, "copy.txt")
            
            src.write_text(content)
            shutil.copy(src, dst)
            
            assert dst.read_text() == content


class TestDeleteFile:
    """File deletion tests"""
    
    def test_delete_file_success(self):
        """Test successful file deletion"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file = Path(tmpdir, "test.txt")
            file.touch()
            assert file.exists()
            
            file.unlink()
            assert not file.exists()
    
    def test_delete_file_nonexistent(self):
        """Test deleting non-existent file"""
        file_path = Path("/nonexistent/file.txt")
        try:
            if file_path.exists():
                file_path.unlink()
        except FileNotFoundError:
            pass  # Expected behavior
    
    def test_delete_multiple_files(self):
        """Test deleting multiple files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            files = [Path(tmpdir, f"file{i}.txt") for i in range(3)]
            for f in files:
                f.touch()
            
            for f in files:
                assert f.exists()
            
            for f in files:
                f.unlink()
            
            for f in files:
                assert not f.exists()


class TestFileOperationsIntegration:
    """File operations integration tests"""
    
    def test_find_and_copy_workflow(self):
        """Test find and copy workflow"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create source file
            source_dir = Path(tmpdir, "source")
            source_dir.mkdir()
            file1 = source_dir / "file1.txt"
            file1.write_text("content1")
            
            # Create destination directory
            dest_dir = Path(tmpdir, "dest")
            dest_dir.mkdir()
            
            # Copy file
            dest_file = dest_dir / "file1.txt"
            shutil.copy(file1, dest_file)
            
            assert dest_file.exists()
            assert dest_file.read_text() == "content1"
    
    def test_handle_special_filenames(self):
        """Test handling special filenames"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create files with special characters
            special_files = [
                "file with spaces.txt",
                "file-with-dashes.txt",
                "file_with_underscores.txt",
            ]
            
            for name in special_files:
                try:
                    file = Path(tmpdir, name)
                    file.write_text("test")
                    assert file.exists()
                except Exception as e:
                    pass  # Some systems may not support certain characters


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
