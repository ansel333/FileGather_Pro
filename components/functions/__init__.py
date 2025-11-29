"""
Functions module for FileGather Pro
Organizes main_window methods into specialized modules by functionality
"""

from .folder_manager import (
    add_search_folder,
    add_drive,
    add_drive_action,
    remove_selected_folders,
    clear_search_folders,
    update_folder_list,
)

from .search_manager import (
    get_search_mode,
    on_gather_mode_changed,
)

from .search_operations import (
    start_search,
    start_exact_search,
    search_folders_by_name,
    _start_folder_search,
    _start_folder_exact_search,
)

from .results_manager import (
    _display_search_results,
    _update_unfound_keywords_display,
    _create_keyword_view_buttons,
    _show_keyword_results,
    show_context_menu,
    show_file_info,
)

from .file_operations_ui import (
    copy_files,
    delete_files,
    generate_pdf_log,
    select_target_folder,
)

from .ui_interactions import (
    add_log,
    open_selected_file,
    open_file_folder,
    show_help,
    cancel_search_action,
)

__all__ = [
    # Folder Manager
    'add_search_folder',
    'add_drive',
    'add_drive_action',
    'remove_selected_folders',
    'clear_search_folders',
    'update_folder_list',
    # Search Manager
    'get_search_mode',
    'on_gather_mode_changed',
    # Search Operations
    'start_search',
    'start_exact_search',
    'search_folders_by_name',
    '_start_folder_search',
    '_start_folder_exact_search',
    # Results Manager
    '_display_search_results',
    '_update_unfound_keywords_display',
    '_create_keyword_view_buttons',
    '_show_keyword_results',
    'show_context_menu',
    'show_file_info',
    # File Operations UI
    'copy_files',
    'delete_files',
    'generate_pdf_log',
    'select_target_folder',
    # UI Interactions
    'add_log',
    'open_selected_file',
    'open_file_folder',
    'show_help',
    'cancel_search_action',
]
