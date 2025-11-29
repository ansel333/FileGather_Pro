"""
Pytest Configuration - Shared fixtures and test setup
"""

import sys
import os

# Set Qt platform IMMEDIATELY before any imports
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
os.environ['QT_DEBUG_PLUGINS'] = '0'
os.environ['QT_XCB_SCREEN_SCALING_FACTOR'] = '1'

import pytest
import tempfile
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def pytest_sessionstart(session):
    """Session initialization hook - runs before pytest starts"""
    # Ensure Qt platform is set
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'

@pytest.fixture
def temp_dir():
    """Provide temporary directory fixture"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def temp_file():
    """Provide temporary file fixture"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("test content\n")
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def sample_text_file():
    """Provide sample text file"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("""
        This is a sample text file
        containing multiple lines
        for testing purposes
        
        Line 4: with some keywords
        Line 5: another test line
        """)
        temp_path = f.name
    
    yield temp_path
    
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def sample_directory_structure():
    """Provide sample directory structure"""
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        
        # Create directory structure
        (base / "documents").mkdir()
        (base / "documents" / "reports").mkdir()
        (base / "images").mkdir()
        (base / "code").mkdir()
        
        # Create files
        (base / "documents" / "readme.txt").write_text("README")
        (base / "documents" / "report1.txt").write_text("Report 1")
        (base / "documents" / "reports" / "report2.txt").write_text("Report 2")
        (base / "images" / "photo.jpg").write_text("fake jpg")
        (base / "code" / "script.py").write_text("print('hello')")
        
        yield base


@pytest.fixture
def mock_search_result():
    """Provide mock search result"""
    return [
        {
            "path": "/path/to/file1.txt",
            "name": "file1.txt",
            "size": 1024,
            "modify_time": "2025-11-29 10:00:00",
            "type": "text"
        },
        {
            "path": "/path/to/file2.pdf",
            "name": "file2.pdf",
            "size": 2048,
            "modify_time": "2025-11-29 11:00:00",
            "type": "pdf"
        },
        {
            "path": "/path/to/folder/file3.docx",
            "name": "file3.docx",
            "size": 4096,
            "modify_time": "2025-11-29 12:00:00",
            "type": "document"
        },
    ]


def pytest_configure(config):
    """Pytest initialization hook"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify collected test items"""
    for item in items:
        # Auto-mark test types
        if "test_" in item.nodeid:
            if "integration" in item.nodeid:
                item.add_marker(pytest.mark.integration)
            else:
                item.add_marker(pytest.mark.unit)


# Configure UTF-8 output
if sys.stdout.encoding.lower() not in ('utf-8', 'utf8'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
