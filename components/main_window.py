"""
主窗口模块
包含主应用程序窗口类 FileGatherPro
所有业务逻辑已提取到 functions 文件夹中
"""

import os
import datetime
from pathlib import Path

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox, 
    QInputDialog, QTreeWidgetItem, QMenu, QAction, QDialog, 
    QScrollArea, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTreeWidget
)

from .ui_builder import UIBuilder
from .utils import register_multilingual_fonts
from .dialogs import FileConflictDialog, PDFLogGenerator

# 导入所有的函数模块
from . import functions


class FileGatherPro(QMainWindow):
    """文件归集管理器主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件归集管理器 - FileGather Pro v2.4.0 | daiyixr & ansel333")
        
        # 设置窗口图标
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            self.setWindowIcon(QIcon())
        
        self.setGeometry(100, 100, 1000, 1050)
        self.setMinimumSize(1000, 850)
        self.setMaximumWidth(1000)

        # 初始化应用程序状态变量
        self._init_state()
        
        # 绑定所有函数模块的方法
        self._bind_functions()
        
        # 注册字体和设置样式
        register_multilingual_fonts()
        self.central_widget = UIBuilder.setup_gradient_background(self)
        
        # 构建UI
        self._build_ui()
        
        # 设置样式表
        self.setStyleSheet(UIBuilder.APP_STYLESHEET)
        
        # 记录启动日志
        self.add_log("启动程序")

    def _bind_functions(self):
        """绑定所有函数模块的方法到类实例"""
        # 文件夹管理方法
        self.add_search_folder = functions.add_search_folder.__get__(self, FileGatherPro)
        self.add_drive = functions.add_drive.__get__(self, FileGatherPro)
        self.add_drive_action = functions.add_drive_action.__get__(self, FileGatherPro)
        self.remove_selected_folders = functions.remove_selected_folders.__get__(self, FileGatherPro)
        self.clear_search_folders = functions.clear_search_folders.__get__(self, FileGatherPro)
        self.update_folder_list = functions.update_folder_list.__get__(self, FileGatherPro)
        
        # 搜索管理方法
        self.get_search_mode = functions.get_search_mode.__get__(self, FileGatherPro)
        self.on_gather_mode_changed = functions.on_gather_mode_changed.__get__(self, FileGatherPro)
        self.cancel_search_action = functions.cancel_search_action.__get__(self, FileGatherPro)
        
        # 搜索操作方法
        self.start_search = functions.start_search.__get__(self, FileGatherPro)
        self.start_exact_search = functions.start_exact_search.__get__(self, FileGatherPro)
        self.search_folders_by_name = functions.search_folders_by_name.__get__(self, FileGatherPro)
        self._start_folder_search = functions._start_folder_search.__get__(self, FileGatherPro)
        self._start_folder_exact_search = functions._start_folder_exact_search.__get__(self, FileGatherPro)
        
        # 结果管理方法
        self._display_search_results = functions._display_search_results.__get__(self, FileGatherPro)
        self._update_unfound_keywords_display = functions._update_unfound_keywords_display.__get__(self, FileGatherPro)
        self._create_keyword_view_buttons = functions._create_keyword_view_buttons.__get__(self, FileGatherPro)
        self._show_keyword_results = functions._show_keyword_results.__get__(self, FileGatherPro)
        self.show_context_menu = functions.show_context_menu.__get__(self, FileGatherPro)
        self.show_file_info = functions.show_file_info.__get__(self, FileGatherPro)
        
        # 文件操作UI方法
        self.copy_files = functions.copy_files.__get__(self, FileGatherPro)
        self.delete_files = functions.delete_files.__get__(self, FileGatherPro)
        self.generate_pdf_log = functions.generate_pdf_log.__get__(self, FileGatherPro)
        self.select_target_folder = functions.select_target_folder.__get__(self, FileGatherPro)
        
        # UI交互方法
        self.add_log = functions.add_log.__get__(self, FileGatherPro)
        self.open_selected_file = functions.open_selected_file.__get__(self, FileGatherPro)
        self.open_file_folder = functions.open_file_folder.__get__(self, FileGatherPro)
        self.show_help = functions.show_help.__get__(self, FileGatherPro)

    def _init_state(self):
        """初始化应用程序状态"""
        self.search_folders = []
        self.search_results = []
        self.target_folder = None
        self.cancel_search = False
        self.operation_log = []
        self.operated_files = set()
        self.found_files_count = 0
        self.keyword_results = {}
        self.unfound_keywords = []
        self.version = "2.4.0"

    def _build_ui(self):
        """构建用户界面"""
        main_components = UIBuilder.build_main_layout(self.version)
        main_layout = main_components[0]
        
        # 保存UI组件引用
        self._extract_ui_components(main_components)
        
        # 设置主布局
        self.central_widget.setLayout(main_layout)
        
        # 连接信号槽
        self._connect_signals()

    def _extract_ui_components(self, main_components):
        """提取UI组件引用"""
        _, _, _, search_comp, button_comp, results_comp, status_label = main_components
        
        # 搜索条件组件
        (self.search_group, self.folder_list, self.add_folder_button, 
         self.add_drive_button, self.remove_folder_button, self.clear_folders_button,
         self.keyword_entry, self.filename_radio, self.content_radio, self.both_radio,
         self.search_mode_group, self.filetype_combo, self.mod_date_combo, 
         self.file_size_combo, self.subfolders_check, self.gather_mode_combo,
         self.filetype_label, self.subfolders_container) = search_comp
        
        # 操作按钮组件
        (_, self.search_button, self.exact_search_button, self.cancel_button, 
         self.target_button, self.copy_button, self.delete_button, self.log_button, 
         self.help_button) = button_comp
        
        # 结果显示组件
        (self.results_group, self.results_tree, self.current_path_label,
         self.progress_bar, self.status_count_label, self.keywords_info_label,
         self.keywords_buttons_container, self.unfound_keywords_group, 
         self.unfound_keywords_text) = results_comp
        
        self.status_label = status_label

    def _connect_signals(self):
        """连接信号和槽"""
        self.add_folder_button.clicked.connect(self.add_search_folder)
        self.add_drive_button.clicked.connect(self.add_drive)
        self.remove_folder_button.clicked.connect(self.remove_selected_folders)
        self.clear_folders_button.clicked.connect(self.clear_search_folders)
        
        self.search_button.clicked.connect(self.start_search)
        self.exact_search_button.clicked.connect(self.start_exact_search)
        self.cancel_button.clicked.connect(self.cancel_search_action)
        
        self.target_button.clicked.connect(self.select_target_folder)
        self.copy_button.clicked.connect(self.copy_files)
        self.delete_button.clicked.connect(self.delete_files)
        self.log_button.clicked.connect(self.generate_pdf_log)
        self.help_button.clicked.connect(self.show_help)
        
        # 归集模式变化时隐藏/显示相关选项
        self.gather_mode_combo.currentIndexChanged.connect(self.on_gather_mode_changed)
        
        self.results_tree.itemDoubleClicked.connect(self.show_file_info)
        self.results_tree.customContextMenuRequested.connect(self.show_context_menu)
