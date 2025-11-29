"""
Unit Tests: Search Logic Module (components.search_logic)
Tests for exact match, keyword matching, and content search functionality
"""

import sys
import os
import pytest
from pathlib import Path
import tempfile

# Set QT_QPA_PLATFORM to offscreen to avoid GUI issues
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.search_logic import exact_match_filename, matches_keyword, search_content


class TestExactMatchFilename:
    """Exact filename matching tests"""
    
    def test_exact_match_with_extension(self):
        """Test exact match with different file extensions"""
        assert exact_match_filename("report.xlsx", "report") is True
        assert exact_match_filename("report.pdf", "report") is True
        assert exact_match_filename("report.docx", "report") is True
        
    def test_exact_match_case_insensitive(self):
        """Test case-insensitive matching"""
        assert exact_match_filename("Report.xlsx", "report") is True
        assert exact_match_filename("REPORT.PDF", "report") is True
        assert exact_match_filename("RePoRt.txt", "REPORT") is True
    
    def test_exact_match_failure(self):
        """Test exact match failure with extra words"""
        assert exact_match_filename("annual_report.xlsx", "report") is False
        assert exact_match_filename("2025report.pdf", "report") is False
        assert exact_match_filename("project_report_summary.docx", "report") is False
    
    def test_exact_match_partial_match_fails(self):
        """Test that partial matches fail"""
        assert exact_match_filename("report_final.xlsx", "report") is False
        assert exact_match_filename("reportv2.pdf", "report") is False
    
    def test_exact_match_empty_keyword(self):
        """Test empty keyword returns True"""
        assert exact_match_filename("any_file.txt", "") is True
        assert exact_match_filename("anything.pdf", "") is True
    
    def test_exact_match_with_numbers(self):
        """Test filename with numbers"""
        assert exact_match_filename("project2024.xlsx", "project2024") is True
        assert exact_match_filename("project2024.pdf", "project") is False
        assert exact_match_filename("2024project.docx", "2024project") is True
    
    def test_exact_match_special_chars(self):
        """Test special character filenames"""
        assert exact_match_filename("file-name.xlsx", "file-name") is True
        assert exact_match_filename("file_name.pdf", "file_name") is True
        assert exact_match_filename("file.name.docx", "file.name") is True


class TestMatchesKeyword:
    """Keyword matching tests"""
    
    def test_simple_keyword_match(self):
        """Test simple keyword matching"""
        assert matches_keyword("this is a test", "test") is True
        assert matches_keyword("this is a test", "another") is False
    
    def test_case_insensitive_match(self):
        """Test case-insensitive matching"""
        assert matches_keyword("Test String", "test") is True
        assert matches_keyword("TEST string", "test") is True
    
    def test_exact_phrase_match(self):
        """Test exact phrase matching with quotes"""
        assert matches_keyword("the quick brown fox", '"quick brown"') is True
        assert matches_keyword("the quick brown fox", '"quick fox"') is False
    
    def test_must_include_keyword(self):
        """Test must include keyword with + prefix"""
        assert matches_keyword("include this and that", "+include +that") is True
        assert matches_keyword("include this only", "+include +that") is False
    
    def test_must_exclude_keyword(self):
        """Test must exclude keyword with - prefix"""
        assert matches_keyword("include this not that", "-exclude") is True
        assert matches_keyword("include this exclude that", "-exclude") is False
    
    def test_or_operator(self):
        """Test OR operator with |"""
        assert matches_keyword("apple or banana", "apple|banana") is True
        assert matches_keyword("apple or banana", "apple|orange") is True
        assert matches_keyword("apple", "apple|banana") is True
        assert matches_keyword("orange", "apple|banana") is False
    
    def test_combined_operators(self):
        """Test combined operators"""
        assert matches_keyword("include this test", "+include test") is True
        assert matches_keyword("include this", "+include -exclude") is True
        assert matches_keyword("exclude this include", "+include -exclude") is False
    
    def test_empty_keyword(self):
        """Test empty keyword"""
        assert matches_keyword("any text", "") is True
        assert matches_keyword("", "") is True
    
    def test_whitespace_handling(self):
        """Test whitespace handling"""
        assert matches_keyword("test string", "test  string") is True
        assert matches_keyword("test\nstring", "test string") is True


class TestSearchContent:
    """Content search tests"""
    
    def test_search_content_in_text_file(self):
        """Test searching content in text file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is a test file\nWith some content\n")
            f.flush()
            temp_path = f.name
        
        try:
            assert search_content(temp_path, "test") is True
            assert search_content(temp_path, "not found") is False
        finally:
            if os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except PermissionError:
                    pass
    
    def test_search_content_case_insensitive(self):
        """Test case-insensitive content search"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("TEST Content\n")
            f.flush()
            temp_path = f.name
        
        try:
            assert search_content(temp_path, "test") is True
            assert search_content(temp_path, "TEST") is True
        finally:
            if os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except PermissionError:
                    pass
    
    def test_search_content_nonexistent_file(self):
        """Test search on non-existent file"""
        result = search_content("/nonexistent/file.txt", "test")
        assert result is False
    
    def test_search_content_empty_file(self):
        """Test search on empty file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.flush()
            temp_path = f.name
        
        try:
            result = search_content(temp_path, "test")
            assert result is False
        finally:
            if os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except PermissionError:
                    pass


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
