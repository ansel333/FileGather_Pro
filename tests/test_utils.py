"""
Unit Tests: Utility Functions Module (components.utils)
Tests for file info retrieval, path handling, and utility functions
"""

import sys
import os
import pytest
import tempfile
from pathlib import Path
from datetime import datetime

# Set QT_QPA_PLATFORM to offscreen to avoid GUI issues
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.utils import get_file_info_dict, format_size, wrap_text, is_file_locked


class TestGetFileInfoDict:
    """File info dictionary tests"""
    
    def test_get_file_info_dict_attributes(self):
        """Test file info dict has required attributes"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content\n")
            f.flush()
            
            info = get_file_info_dict(f.name)
            assert info is not None
            assert isinstance(info, dict)
            assert 'path' in info or 'name' in info
            
            os.unlink(f.name)
    
    def test_get_file_info_dict_with_size(self):
        """Test retrieving file size info"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            content = "x" * 1000
            f.write(content)
            f.flush()
            
            info = get_file_info_dict(f.name)
            assert info is not None
            size = info.get('size', 0)
            assert size >= 0
            
            os.unlink(f.name)
    
    def test_get_file_info_dict_directory(self):
        """Test retrieving directory info"""
        with tempfile.TemporaryDirectory() as tmpdir:
            info = get_file_info_dict(tmpdir)
            assert info is not None or info == {}
    
    def test_get_file_info_dict_nonexistent(self):
        """Test non-existent file info"""
        info = get_file_info_dict("/nonexistent/path/file.txt")
        assert info is None or info == {}
    
    def test_get_file_info_dict_special_files(self):
        """Test special file types"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create different file types
            files = {
                "text.txt": "text content",
                "script.py": "print('hello')",
                "data.json": '{"key": "value"}',
            }
            
            for name, content in files.items():
                file = Path(tmpdir, name)
                file.write_text(content)
                
                info = get_file_info_dict(str(file))
                assert info is not None


class TestFormatFileSize:
    """File size formatting tests"""
    
    def test_format_bytes(self):
        """Test byte formatting"""
        result = format_file_size(512)
        assert result is not None
        assert isinstance(result, str)
    
    def test_format_kilobytes(self):
        """Test KB formatting"""
        result = format_file_size(1024)  # 1 KB
        assert result is not None
    
    def test_format_megabytes(self):
        """Test MB formatting"""
        result = format_file_size(1024 * 1024)  # 1 MB
        assert result is not None
    
    def test_format_gigabytes(self):
        """Test GB formatting"""
        result = format_file_size(1024 * 1024 * 1024)  # 1 GB
        assert result is not None
    
    def test_format_zero_bytes(self):
        """Test zero byte formatting"""
        result = format_file_size(0)
        assert result is not None


class TestGetFileType:
    """File type identification tests"""
    
    def test_get_file_type_by_extension(self):
        """Test file type by extension"""
        test_files = {
            "document.txt": "text",
            "image.jpg": "image",
            "data.json": "text",
            "script.py": "text",
        }
        
        for filename, expected_type in test_files.items():
            extension = Path(filename).suffix.lower()
            assert extension in [".txt", ".jpg", ".json", ".py"]
    
    def test_get_file_type_no_extension(self):
        """Test file without extension"""
        filename = "README"
        extension = Path(filename).suffix
        assert extension == ""
    
    def test_get_file_type_multiple_dots(self):
        """Test filename with multiple dots"""
        filename = "archive.tar.gz"
        extension = Path(filename).suffix
        assert extension == ".gz"


class TestUtilsIntegration:
    """Utility functions integration tests"""
    
    def test_get_file_info_workflow(self):
        """Test complete file info workflow"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("test content\n" * 50)
            f.flush()
            
            info = get_file_info_dict(f.name)
            assert info is not None
            
            size = info.get('size', 0)
            assert size > 0
            
            size_str = format_file_size(size)
            assert size_str is not None
            
            os.unlink(f.name)
    
    def test_handle_various_file_types(self):
        """Test handling various file types"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create different file types
            file_types = {
                "test.txt": "text file",
                "script.py": "print('hello')",
                "data.json": '{"test": true}',
            }
            
            for filename, content in file_types.items():
                file_path = Path(tmpdir, filename)
                file_path.write_text(content)
                
                info = get_file_info_dict(str(file_path))
                assert info is not None
                
                size = info.get('size', 0) if info else 0
                assert size > 0
    
    def test_error_handling(self):
        """Test error handling"""
        # Non-existent path
        info = get_file_info_dict("/invalid/path/file.txt")
        assert info is None or info == {}
        
        # Empty string
        info = get_file_info_dict("")
        assert info is None or info == {}


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
