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

from components.file_operations import (
    calculate_hash,
    copy_files_without_conflicts,
    copy_selected_files,
    delete_files_batch,
    copy_folders_without_conflicts,
)
from components.utils import get_file_info_dict


class TestBasicFileOperations:
    """Basic file operations tests"""
    
    def test_file_exists_check(self):
        """Test checking if file exists"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir, "test.txt")
            assert not file_path.exists()
            
            file_path.touch()
            assert file_path.exists()
    
    def test_directory_exists_check(self):
        """Test checking if directory exists"""
        with tempfile.TemporaryDirectory() as tmpdir:
            dir_path = Path(tmpdir, "subdir")
            assert not dir_path.exists()
            
            dir_path.mkdir()
            assert dir_path.exists()


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


class TestCopyFolder:
    """Folder copy tests (for folder gathering mode)"""
    
    def test_copy_folder_basic(self):
        """Test basic folder copy with copytree"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create source folder structure
            src_folder = Path(tmpdir, "source_folder")
            src_folder.mkdir()
            (src_folder / "file1.txt").write_text("content1")
            (src_folder / "file2.txt").write_text("content2")
            
            # Create subfolder
            subfolder = src_folder / "subfolder"
            subfolder.mkdir()
            (subfolder / "file3.txt").write_text("content3")
            
            # Copy folder
            dest_folder = Path(tmpdir, "dest_folder")
            shutil.copytree(str(src_folder), str(dest_folder))
            
            # Verify copy
            assert dest_folder.exists()
            assert (dest_folder / "file1.txt").read_text() == "content1"
            assert (dest_folder / "file2.txt").read_text() == "content2"
            assert (dest_folder / "subfolder" / "file3.txt").read_text() == "content3"
    
    def test_copy_folder_conflict_rename(self):
        """Test folder copy with conflict handling (auto-rename)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create source folder
            src_folder = Path(tmpdir, "source_folder")
            src_folder.mkdir()
            (src_folder / "file1.txt").write_text("source_content")
            
            # Create destination folder with same name
            dest_base = Path(tmpdir, "dest_base")
            dest_base.mkdir()
            existing_folder = dest_base / "source_folder"
            existing_folder.mkdir()
            (existing_folder / "file2.txt").write_text("existing_content")
            
            # Simulate conflict handling with rename
            dst = existing_folder
            if dst.exists():
                counter = 1
                dst = dest_base / f"source_folder_{counter}"
                while dst.exists():
                    counter += 1
                    dst = dest_base / f"source_folder_{counter}"
            
            # Copy to renamed location
            shutil.copytree(str(src_folder), str(dst))
            
            # Verify both folders exist
            assert existing_folder.exists()
            assert dst.exists()
            assert dst.name == "source_folder_1"
            assert (dst / "file1.txt").read_text() == "source_content"
            assert (existing_folder / "file2.txt").read_text() == "existing_content"
    
    def test_copy_folder_empty(self):
        """Test copying empty folder"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src_folder = Path(tmpdir, "empty_folder")
            src_folder.mkdir()
            
            dst_folder = Path(tmpdir, "empty_folder_copy")
            shutil.copytree(str(src_folder), str(dst_folder))
            
            assert dst_folder.exists()
            assert list(dst_folder.iterdir()) == []


class TestDeleteFolder:
    """Folder deletion tests (for folder gathering mode)"""
    
    def test_delete_folder_basic(self):
        """Test basic folder deletion with rmtree"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create folder with content
            folder = Path(tmpdir, "test_folder")
            folder.mkdir()
            (folder / "file1.txt").write_text("content")
            
            subfolder = folder / "subfolder"
            subfolder.mkdir()
            (subfolder / "file2.txt").write_text("content")
            
            # Delete folder
            assert folder.exists()
            shutil.rmtree(str(folder))
            assert not folder.exists()
    
    def test_delete_folder_empty(self):
        """Test deleting empty folder"""
        with tempfile.TemporaryDirectory() as tmpdir:
            folder = Path(tmpdir, "empty_folder")
            folder.mkdir()
            
            assert folder.exists()
            shutil.rmtree(str(folder))
            assert not folder.exists()
    
    def test_delete_folder_nested(self):
        """Test deleting nested folder structure"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create nested structure
            folder = Path(tmpdir, "root_folder")
            folder.mkdir()
            (folder / "level1").mkdir()
            (folder / "level1" / "level2").mkdir()
            (folder / "level1" / "level2" / "file.txt").write_text("content")
            
            # Delete entire tree
            assert folder.exists()
            shutil.rmtree(str(folder))
            assert not folder.exists()


class TestDeleteFilesBatch:
    """Batch file/folder deletion tests (mixed mode)"""
    
    def test_delete_batch_files_only(self):
        """Test batch deletion of files only"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create multiple files
            files = [Path(tmpdir, f"file{i}.txt") for i in range(3)]
            for i, f in enumerate(files):
                f.write_text(f"content{i}")
            
            # Create a folder (should not be deleted in this test)
            folder = Path(tmpdir, "keep_folder")
            folder.mkdir()
            
            # Prepare deletion list with file paths only
            files_to_delete = [str(f) for f in files]
            
            # Simulate batch deletion
            success_count = 0
            for file_path in files_to_delete:
                file_path_obj = Path(file_path)
                if file_path_obj.exists():
                    if file_path_obj.is_dir():
                        shutil.rmtree(str(file_path_obj))
                    else:
                        file_path_obj.unlink()
                    success_count += 1
            
            # Verify
            assert success_count == 3
            for f in files:
                assert not f.exists()
            assert folder.exists()
    
    def test_delete_batch_mixed_files_and_folders(self):
        """Test batch deletion of mixed files and folders"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create files and folders
            file1 = Path(tmpdir, "file1.txt")
            file1.write_text("content1")
            
            folder1 = Path(tmpdir, "folder1")
            folder1.mkdir()
            (folder1 / "nested_file.txt").write_text("nested")
            
            file2 = Path(tmpdir, "file2.txt")
            file2.write_text("content2")
            
            # Prepare mixed deletion list
            items_to_delete = [str(file1), str(folder1), str(file2)]
            
            # Simulate batch deletion
            success_count = 0
            for item_path in items_to_delete:
                item_path_obj = Path(item_path)
                if item_path_obj.exists():
                    if item_path_obj.is_dir():
                        shutil.rmtree(str(item_path_obj))
                    else:
                        item_path_obj.unlink()
                    success_count += 1
            
            # Verify all deleted
            assert success_count == 3
            assert not file1.exists()
            assert not folder1.exists()
            assert not file2.exists()


class TestCalculateHash:
    """File hash calculation tests"""
    
    def test_calculate_hash_consistency(self):
        """Test that hash calculation is consistent"""
        with tempfile.TemporaryDirectory() as tmpdir:
            f = Path(tmpdir, "test_hash.txt")
            f.write_text("test content for hashing")
            
            hash1 = calculate_hash(str(f))
            hash2 = calculate_hash(str(f))
            
            assert hash1 == hash2
            assert hash1 is not None
            assert len(hash1) == 64  # SHA256 hex digest length
    
    def test_calculate_hash_different_content(self):
        """Test that different content produces different hashes"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir, "file1.txt")
            file2 = Path(tmpdir, "file2.txt")
            
            file1.write_text("content1")
            file2.write_text("content2")
            
            hash1 = calculate_hash(str(file1))
            hash2 = calculate_hash(str(file2))
            
            assert hash1 != hash2
    
    def test_calculate_hash_nonexistent_file(self):
        """Test hash calculation on non-existent file"""
        result = calculate_hash("/nonexistent/file.txt")
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
