"""
FileGather Pro Components Package
包含所有应用组件模块
"""

from .ui_builder import UIBuilder
from .utils import (
    register_multilingual_fonts,
    format_size,
    wrap_text,
    extract_filename_for_log,
    is_file_locked,
    get_file_info_dict
)
from .search_logic import (
    matches_keyword,
    search_content,
    search_text_file,
    search_pdf,
    search_docx,
    search_excel
)
from .file_operations import (
    calculate_hash,
    copy_files_without_conflicts,
    copy_selected_files,
    delete_files_batch
)
from .dialogs import (
    KeywordSearchResultDialog,
    FileConflictDialog,
    PDFLogGenerator
)
from .main_window import FileGatherPro

__all__ = [
    'UIBuilder',
    'register_multilingual_fonts',
    'format_size',
    'wrap_text',
    'extract_filename_for_log',
    'is_file_locked',
    'get_file_info_dict',
    'matches_keyword',
    'search_content',
    'search_text_file',
    'search_pdf',
    'search_docx',
    'search_excel',
    'calculate_hash',
    'copy_files_without_conflicts',
    'copy_selected_files',
    'delete_files_batch',
    'KeywordSearchResultDialog',
    'FileConflictDialog',
    'PDFLogGenerator',
    'FileGatherPro'
]
