"""
UI 构建器模块
负责构建应用程序的所有UI组件
"""

import datetime
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QColor, QPalette, QLinearGradient, QBrush, QFont, QAction
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QCheckBox, QGroupBox, QFileDialog,
    QMessageBox, QTreeWidget, QProgressBar, QListWidget,
    QTextEdit, QRadioButton, QButtonGroup, QHeaderView, QAbstractItemView,
    QMenu, QPlainTextEdit
)


class UIBuilder:
    """UI构建器类，负责创建和管理所有UI组件"""
    
    # 应用程序样式表
    APP_STYLESHEET = """
        QGroupBox {
            font-weight: bold;
            border: 1px solid #3498db;
            border-radius: 5px;
            margin-top: 1ex;
            background-color: rgba(255, 255, 255, 180);
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 5px;
            color: #2980b9;
        }
        QPushButton {
            background-color: white;
            color: #2c3e50;
            border: 2px solid #3498db;
            padding: 4px 8px;
            border-radius: 5px;
            font-weight: 600;
            font-size: 9pt;
            min-height: 22px;
            min-width: 65px;
        }
        QPushButton:hover {
            background-color: #ecf0f1;
            border: 2px solid #2980b9;
            color: #2c3e50;
        }
        QPushButton:pressed {
            background-color: #d5dbdb;
            border: 2px solid #1c6ea4;
            color: #1c6ea4;
        }
        QPushButton:disabled {
            background-color: #ecf0f1;
            color: #95a5a6;
            border: 2px solid #bdc3c7;
        }
        QTreeWidget {
            background-color: rgba(255, 255, 255, 200);
            border: 1px solid #3498db;
            border-radius: 3px;
        }
        QLineEdit, QComboBox, QDateEdit {
            padding: 5px;
            border: 1px solid #3498db;
            border-radius: 3px;
            background-color: rgba(255, 255, 255, 200);
        }
        QProgressBar {
            border: 1px solid #3498db;
            border-radius: 3px;
            text-align: center;
            background-color: rgba(255, 255, 255, 200);
        }
        QProgressBar::chunk {
            background-color: #3498db;
            width: 10px;
        }
        QListWidget {
            background-color: rgba(255, 255, 255, 200);
            border: 1px solid #3498db;
            border-radius: 3px;
        }
        QRadioButton {
            padding: 4px;
        }
    """
    
    @staticmethod
    def setup_gradient_background(window):
        """设置窗口渐变背景"""
        central_widget = QWidget()
        window.setCentralWidget(central_widget)

        palette = window.palette()
        gradient = QLinearGradient(0, 0, 0, window.height())
        gradient.setColorAt(0, QColor(230, 245, 255))
        gradient.setColorAt(1, QColor(180, 220, 255))
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        window.setPalette(palette)
        
        return central_widget

    @staticmethod
    def build_title_widgets(version):
        """构建标题和版本信息小部件"""
        title_label = QLabel("文件归集管理器")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50;")

        version_label = QLabel(f"版本: V{version} | © 2025 D&Ai/2FX 文件归集管理器")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet("color: #7f8c8d; font-size: 8pt;")
        
        return title_label, version_label

    @staticmethod
    def build_search_conditions_group():
        """构建搜索条件群组"""
        search_group = QGroupBox("搜索条件")
        search_layout = QVBoxLayout()
        search_layout.setSpacing(6)
        search_layout.setContentsMargins(8, 8, 8, 8)

        # 文件夹管理部分
        folder_layout = QVBoxLayout()
        folder_layout.setSpacing(4)
        folder_label = QLabel("搜索文件夹:")
        
        folder_list = QListWidget()
        folder_list.setMaximumHeight(50)

        folder_button_layout = QHBoxLayout()
        folder_button_layout.setSpacing(4)
        add_folder_button = QPushButton("添加文件夹")
        add_drive_button = QPushButton("添加盘符")
        remove_folder_button = QPushButton("删除选中")
        clear_folders_button = QPushButton("清空列表")

        folder_button_layout.addWidget(add_folder_button)
        folder_button_layout.addWidget(add_drive_button)
        folder_button_layout.addWidget(remove_folder_button)
        folder_button_layout.addWidget(clear_folders_button)

        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(folder_list)
        folder_layout.addLayout(folder_button_layout)
        search_layout.addLayout(folder_layout)

        # 关键词部分
        keyword_layout = QHBoxLayout()
        keyword_layout.setSpacing(5)
        keyword_label = QLabel("关键词:")
        keyword_entry = QTextEdit()
        keyword_entry.setPlaceholderText("输入文件名包含的关键词，支持多行输入")
        keyword_entry.setFixedHeight(48)
        keyword_entry.setToolTip(
            "支持多种搜索模式：\n"
            "- 基本搜索: 输入关键词，如 \"报告\"\n"
            "- 多关键词: 用空格或换行分隔多个关键词，如 \"报告 2025\"\n"
            "- 逻辑与: 使用 \"+\" 表示必须包含，如 \"+重要 +财务\"\n"
            "- 逻辑或: 使用 \"|\" 表示或关系，如 \"报告|总结\"\n"
            "- 排除: 使用 \"-\" 排除关键词，如 \"报告 -草稿\"\n"
            "- 通配符: 使用 \"*\" 匹配任意字符，如 \"项目*报告\"\n"
            "- 精确匹配: 使用引号进行精确匹配，如 \"\\\"季度报告\\\"\"\n"
            "\n示例: \"项目 +最终版 -草稿\" 表示搜索包含\"项目\"和\"最终版\"但不包含\"草稿\"的文件"
        )

        keyword_layout.addWidget(keyword_label)
        keyword_layout.addWidget(keyword_entry, 1)
        search_layout.addLayout(keyword_layout)

        # 搜索模式和归集模式部分
        search_mode_layout = QHBoxLayout()
        search_mode_layout.setSpacing(6)
        search_mode_label = QLabel("搜索模式:")

        search_mode_group = QButtonGroup()
        filename_radio = QRadioButton("仅文件名")
        content_radio = QRadioButton("仅内容")
        both_radio = QRadioButton("两者同时")
        filename_radio.setChecked(True)

        tooltip = (
            "选择搜索模式：\n"
            "- 仅文件名: 只在文件名中匹配关键词\n"
            "- 仅内容: 只在文件内容中匹配关键词\n"
            "- 两者同时: 在文件名或内容中匹配关键词即可\n\n"
            "注意：内容搜索仅检查文件的前3000个字符"
        )
        filename_radio.setToolTip(tooltip)
        content_radio.setToolTip(tooltip)
        both_radio.setToolTip(tooltip)

        search_mode_layout.addWidget(search_mode_label)
        search_mode_layout.addWidget(filename_radio)
        search_mode_layout.addWidget(content_radio)
        search_mode_layout.addWidget(both_radio)
        
        # 添加分隔符
        separator = QLabel("|")
        search_mode_layout.addWidget(separator)
        
        # 添加归集模式下拉框
        gather_mode_label = QLabel("归集模式:")
        gather_mode_combo = QComboBox()
        gather_mode_combo.addItem("文件归集", "file")
        gather_mode_combo.addItem("文件夹归集", "folder")
        gather_mode_combo.setToolTip(
            "选择归集模式：\n"
            "- 文件归集: 搜索并归集匹配的文件\n"
            "- 文件夹归集: 搜索并归集第一级子目录\n\n"
            "文件夹归集模式会自动隐藏子文件夹和文件类型选项"
        )
        
        search_mode_layout.addWidget(gather_mode_label)
        search_mode_layout.addWidget(gather_mode_combo)
        search_mode_layout.addStretch(1)

        search_layout.addLayout(search_mode_layout)

        # 文件类型部分
        filetype_layout = QHBoxLayout()
        filetype_layout.setSpacing(5)
        filetype_label = QLabel("文件类型:")
        filetype_combo = QComboBox()
        filetype_combo.addItem("所有文件", "")
        filetype_combo.addItem("文档", [".doc", ".docx", ".txt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"])
        filetype_combo.addItem("图片", [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"])
        filetype_combo.addItem("视频", [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".mpg"])
        filetype_combo.addItem("音频", [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"])
        filetype_combo.addItem("可执行文件", [".exe", ".msi", ".bat", ".cmd"])
        filetype_combo.addItem("压缩文件", [".zip", ".rar", ".7z", ".tar", ".gz"])
        filetype_combo.addItem("自定义", "custom")
        filetype_combo.setToolTip(
            "选择要搜索的文件类型：\n"
            "- 所有文件: 搜索功能所有类型的文件\n"
            "- 文档: 包括 .doc, .docx, .txt, .pdf 等\n"
            "- 图片: 包括 .jpg, .jpeg, .png, .gif 等\n"
            "- 视频: 包括 .mp4, .avi, .mov, .mkv 等\n"
            "- 音频: 包括 .mp3, .wav, .flac, .aac 等\n"
            "- 可执行文件: 包括 .exe, .msi, .bat, .cmd 等\n"
            "- 压缩文件: 包括 .zip, .rar, .7z, .tar 等\n"
            "- 自定义: 手动输入扩展名，用分号分隔，如 \".py;.java;.cpp\""
        )

        filetype_layout.addWidget(filetype_label)
        filetype_layout.addWidget(filetype_combo, 1)
        search_layout.addLayout(filetype_layout)

        # 日期和大小部分
        date_size_layout = QHBoxLayout()
        date_size_layout.setSpacing(10)

        mod_date_layout = QVBoxLayout()
        mod_date_layout.setSpacing(3)
        mod_date_label = QLabel("修改日期:")
        mod_date_combo = QComboBox()
        mod_date_combo.addItem("不限", (None, None))
        mod_date_combo.addItem("今天", (datetime.date.today(), datetime.date.today()))
        mod_date_combo.addItem("最近7天", (datetime.date.today() - datetime.timedelta(days=7), datetime.date.today()))
        mod_date_combo.addItem("最近30天", (datetime.date.today() - datetime.timedelta(days=30), datetime.date.today()))
        mod_date_combo.addItem("自定义...", "custom")
        mod_date_combo.setToolTip(
            "按文件最后修改日期筛选：\n"
            "- 不限: 不限制修改日期\n"
            "- 今天: 只搜索今天修改过的文件\n"
            "- 最近7天: 搜索按钮7天内修改的文件\n"
            "- 最近30天: 30天内修改的文件\n"
            "- 自定义: 手动设置日期范围\n\n"
            "注意：此筛选基于文件的最后修改时间"
        )

        mod_date_layout.addWidget(mod_date_label)
        mod_date_layout.addWidget(mod_date_combo)
        date_size_layout.addLayout(mod_date_layout)

        file_size_layout = QVBoxLayout()
        file_size_layout.setSpacing(3)
        file_size_label = QLabel("文件大小:")
        file_size_combo = QComboBox()
        file_size_combo.addItem("不限", (0, float('inf')))
        file_size_combo.addItem("小于 1MB", (0, 1024 * 1024))
        file_size_combo.addItem("1MB - 10MB", (1024 * 1024, 10 * 1024 * 1024))
        file_size_combo.addItem("大于 10MB", (10 * 1024 * 1024, float('inf')))
        file_size_combo.setToolTip(
            "按文件大小范围筛选：\n"
            "- 不限: 不限制文件大小\n"
            "- 小于 1MB: 功能筛选小于1MB的文件\n"
            "- 1MB - 10MB: 功能筛选1MB到10MB之间的文件\n"
            "- 大于 10MB: 大于10MB的文件\n\n"
            "注意：1MB = 1024KB = 1,048,576字节"
        )

        file_size_layout.addWidget(file_size_label)
        file_size_layout.addWidget(file_size_combo)
        date_size_layout.addLayout(file_size_layout)

        # 创建包含子文件夹的容器以便于在文件夹归集模式下隐藏
        subfolders_container = QWidget()
        subfolders_layout = QHBoxLayout()
        subfolders_layout.setContentsMargins(0, 0, 0, 0)
        subfolders_label = QLabel("包含子文件夹:")
        subfolders_check = QCheckBox()
        subfolders_check.setChecked(True)
        subfolders_layout.addWidget(subfolders_label)
        subfolders_layout.addWidget(subfolders_check)
        subfolders_layout.addStretch()
        subfolders_container.setLayout(subfolders_layout)
        
        search_layout.addWidget(subfolders_container)
        search_layout.addLayout(date_size_layout)

        search_group.setLayout(search_layout)
        
        return (search_group, folder_list, add_folder_button, add_drive_button, 
                remove_folder_button, clear_folders_button, keyword_entry, 
                filename_radio, content_radio, both_radio, search_mode_group,
                filetype_combo, mod_date_combo, file_size_combo, subfolders_check,
                gather_mode_combo, filetype_label, subfolders_container)

    @staticmethod
    def build_action_buttons():
        """构建操作按钮 - 八个按钮一行居中对齐"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(3)
        button_layout.setContentsMargins(0, 2, 0, 2)
        button_layout.addStretch(1)
        
        search_button = QPushButton("模糊查找")
        search_button.setFixedSize(75, 26)
        search_button.setToolTip("搜索包含关键词的文件（默认模式）")
        
        exact_search_button = QPushButton("精确查找")
        exact_search_button.setFixedSize(75, 26)
        exact_search_button.setToolTip("搜索文件名完全匹配关键词的文件")
        
        target_button = QPushButton("选择目标")
        target_button.setFixedSize(75, 26)
        target_button.setToolTip("设置文件复制的目标文件夹")
        
        copy_button = QPushButton("开始归集")
        copy_button.setFixedSize(75, 26)
        copy_button.setEnabled(False)
        copy_button.setToolTip("将找到的文件复制到目标文件夹")
        
        delete_button = QPushButton("删除原文件")
        delete_button.setFixedSize(75, 26)
        delete_button.setEnabled(False)
        delete_button.setToolTip("删除已复制的原始文件")
        
        log_button = QPushButton("生成日志")
        log_button.setFixedSize(75, 26)
        log_button.setEnabled(True)
        log_button.setToolTip("生成搜索和操作日志的PDF报告")
        
        help_button = QPushButton("使用说明")
        help_button.setFixedSize(75, 26)
        help_button.setToolTip("查看应用使用说明")
        
        cancel_button = QPushButton("取消搜索")
        cancel_button.setFixedSize(75, 26)
        cancel_button.setEnabled(False)
        cancel_button.setToolTip("停止当前搜索")
        
        button_layout.addWidget(search_button)
        button_layout.addWidget(exact_search_button)
        button_layout.addWidget(target_button)
        button_layout.addWidget(copy_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(log_button)
        button_layout.addWidget(help_button)
        button_layout.addWidget(cancel_button)
        button_layout.addStretch(1)

        return (button_layout, search_button, exact_search_button, cancel_button, target_button, 
                copy_button, delete_button, log_button, help_button)

    @staticmethod
    def build_results_group():
        """构建搜索结果群组"""
        results_group = QGroupBox("搜索结果")
        results_layout = QVBoxLayout()
        results_layout.setSpacing(5)
        results_layout.setContentsMargins(8, 8, 8, 8)

        results_tree = QTreeWidget()
        results_tree.setHeaderLabels(["文件名", "路径", "大小", "修改日期", "匹配关键词"])
        results_tree.setColumnWidth(0, 180)
        results_tree.setColumnWidth(1, 250)
        results_tree.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        results_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        results_tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        results_tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        results_tree.header().setStretchLastSection(False)
        results_tree.setMinimumHeight(80)

        results_layout.addWidget(results_tree)

        current_path_label = QLabel("当前搜索路径: ")
        current_path_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        results_layout.addWidget(current_path_label)

        progress_bar = QProgressBar()
        progress_bar.setVisible(False)
        results_layout.addWidget(progress_bar)

        status_layout = QHBoxLayout()
        status_count_label = QLabel("已找到: 0 个文件")
        status_count_label.setStyleSheet("font-weight: bold; color: #2980b9;")
        status_layout.addWidget(status_count_label)
        status_layout.addStretch(1)

        results_layout.addLayout(status_layout)
        
        # 关键词统计信息
        keywords_info_label = QLabel()
        keywords_info_label.setStyleSheet("color: #7f8c8d; font-size: 9pt;")
        keywords_info_label.setWordWrap(True)
        keywords_info_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard)
        keywords_info_label.setCursor(Qt.CursorShape.IBeamCursor)
        results_layout.addWidget(keywords_info_label)
        
        # 关键词查看按钮容器
        keywords_buttons_container = QWidget()
        keywords_buttons_layout = QHBoxLayout()
        keywords_buttons_layout.setContentsMargins(0, 5, 0, 0)
        keywords_buttons_layout.setSpacing(5)
        keywords_buttons_container.setLayout(keywords_buttons_layout)
        results_layout.addWidget(keywords_buttons_container)
        
        # 未找到结果的关键词显示区域
        unfound_keywords_group = QGroupBox("未找到结果的关键词")
        unfound_keywords_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #e74c3c;
                border-radius: 5px;
                margin-top: 1ex;
                background-color: rgba(255, 250, 250, 180);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
        """)
        unfound_keywords_layout = QVBoxLayout()
        unfound_keywords_text = QPlainTextEdit()
        unfound_keywords_text.setMaximumHeight(100)
        unfound_keywords_text.setReadOnly(True)
        unfound_keywords_text.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        unfound_keywords_layout.addWidget(unfound_keywords_text)
        unfound_keywords_group.setLayout(unfound_keywords_layout)
        unfound_keywords_group.setVisible(False)
        results_layout.addWidget(unfound_keywords_group)

        results_group.setLayout(results_layout)

        return (results_group, results_tree, current_path_label, 
                progress_bar, status_count_label, keywords_info_label, keywords_buttons_container,
                unfound_keywords_group, unfound_keywords_text)

    @staticmethod
    def build_main_layout(version):
        """构建主布局"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(12, 12, 12, 12)

        # 标题
        title_label, version_label = UIBuilder.build_title_widgets(version)
        main_layout.addWidget(title_label)
        main_layout.addWidget(version_label)

        # 搜索条件
        search_components = UIBuilder.build_search_conditions_group()
        main_layout.addWidget(search_components[0])

        # 操作按钮
        button_components = UIBuilder.build_action_buttons()
        main_layout.addLayout(button_components[0])

        # 搜索结果
        results_components = UIBuilder.build_results_group()
        main_layout.addWidget(results_components[0], 1)

        # 状态栏
        status_label = QLabel("就绪")
        status_label.setStyleSheet("color: #7f8c8d; font-size: 9pt;")
        main_layout.addWidget(status_label)

        return (main_layout, title_label, version_label, search_components, 
                button_components, results_components, status_label)
