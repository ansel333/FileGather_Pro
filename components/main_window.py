"""
主窗口模块
包含主应用程序窗口类 FileGatherPro
"""

import os
import datetime
import re
from pathlib import Path

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox, 
    QInputDialog, QTreeWidgetItem, QMenu, QAction, QDialog, 
    QScrollArea, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTreeWidget
)

from .ui_builder import UIBuilder
from .utils import (
    register_multilingual_fonts, format_size, is_file_locked,
    extract_filename_for_log, wrap_text, get_file_info_dict
)
from .search_logic import matches_keyword, search_content, exact_match_filename
from .file_operations import copy_files_without_conflicts, copy_selected_files, delete_files_batch
from .dialogs import FileConflictDialog, PDFLogGenerator


class FileGatherPro(QMainWindow):
    """文件归集管理器主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件归集管理器 - FileGather Pro v2.3.5.1 | daiyixr & ansel333")
        
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
        
        # 注册字体和设置样式
        register_multilingual_fonts()
        self.central_widget = UIBuilder.setup_gradient_background(self)
        
        # 构建UI
        self._build_ui()
        
        # 设置样式表
        self.setStyleSheet(UIBuilder.APP_STYLESHEET)
        
        # 记录启动日志
        self.add_log("启动程序")

    def _init_state(self):
        """初始化应用程序状态"""
        self.search_results = []
        self.target_folder = ""
        self.version = "2.3.5.1"
        self.update_log = "完成代码重构，改进易读性和组织性 (2025-11-29)"
        self.search_folders = []
        self.found_files_count = 0
        self.searching = False
        self.cancel_search = False
        self.operation_log = []
        self.operated_files = set()
        self.keyword_results = {}  # 存储关键词搜索结果
        self.unfound_keywords = []  # 存储没有找到结果的关键词

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
         self.file_size_combo, self.subfolders_check) = search_comp
        
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
        """连接信号槽"""
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
        
        self.results_tree.itemDoubleClicked.connect(self.show_file_info)
        self.results_tree.customContextMenuRequested.connect(self.show_context_menu)

    # =============== 日志管理 ===============
    
    def add_log(self, action, file_path=None):
        """添加操作日志"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.operation_log.append(f"{timestamp} - {action}")
        if file_path:
            self.operated_files.add(str(file_path))

    # =============== 文件夹管理 ===============
    
    def add_search_folder(self):
        """添加搜索文件夹"""
        folder = QFileDialog.getExistingDirectory(self, "选择搜索文件夹")
        if folder and folder not in self.search_folders:
            self.search_folders.append(folder)
            self.update_folder_list()
            self.add_log(f"添加搜索文件夹: {folder}", folder)

    def add_drive(self):
        """添加盘符"""
        from PyQt5.QtWidgets import QMenu, QAction
        
        drives = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if Path(f"{d}:").exists()]
        if not drives:
            QMessageBox.information(self, "信息", "未找到可用盘符")
            return

        menu = QMenu(self)
        for drive in drives:
            action = QAction(drive, self)
            action.triggered.connect(lambda checked, d=drive: self.add_drive_action(d))
            menu.addAction(action)

        pos = self.add_drive_button.mapToGlobal(QPoint(0, self.add_drive_button.height()))
        menu.exec_(pos)

    def add_drive_action(self, drive):
        """添加盘符到搜索列表"""
        if drive not in self.search_folders:
            self.search_folders.append(drive)
            self.update_folder_list()
            self.add_log(f"添加盘符: {drive}", drive)

    def remove_selected_folders(self):
        """删除选中的文件夹"""
        selected_items = self.folder_list.selectedItems()
        if not selected_items:
            return

        for item in selected_items:
            folder = item.text()
            if folder in self.search_folders:
                self.search_folders.remove(folder)
                self.add_log("删除选中的搜索文件夹", folder)

        self.update_folder_list()

    def clear_search_folders(self):
        """清空所有搜索文件夹"""
        self.search_folders = []
        self.update_folder_list()
        self.add_log("清空搜索文件夹列表")

    def update_folder_list(self):
        """更新文件夹列表显示"""
        self.folder_list.clear()
        for folder in self.search_folders:
            self.folder_list.addItem(folder)

    # =============== 搜索模式 ===============
    
    def get_search_mode(self):
        """获取当前搜索模式"""
        if self.filename_radio.isChecked():
            return "filename"
        elif self.content_radio.isChecked():
            return "content"
        elif self.both_radio.isChecked():
            return "both"
        return "filename"

    def cancel_search_action(self):
        """取消搜索"""
        self.cancel_search = True
        self.status_label.setText("搜索已取消")
        self.cancel_button.setEnabled(False)
        self.search_button.setEnabled(True)
        self.exact_search_button.setEnabled(True)
        self.add_log("取消搜索")

    def start_exact_search(self):
        """开始精确搜索 - 文件名必须严格匹配"""
        if not self.search_folders:
            QMessageBox.warning(self, "错误", "请添加至少一个搜索文件夹或盘符！")
            return

        self.cancel_button.setEnabled(True)
        self.cancel_search = False

        keywords_text = self.keyword_entry.toPlainText().strip()
        keywords = [kw.strip() for kw in re.split(r'[\s\n]+', keywords_text) if kw.strip()]

        if not keywords:
            QMessageBox.warning(self, "提示", "请输入至少一个关键词。")
            self.exact_search_button.setEnabled(True)
            self.cancel_button.setEnabled(False)
            return

        file_types = self.filetype_combo.currentData()
        include_subfolders = self.subfolders_check.isChecked()

        self.add_log(f"开始精确搜索，关键词: {', '.join(keywords)}，文件类型: {self.filetype_combo.currentText()}")

        if file_types == "custom":
            custom_types, ok = QInputDialog.getText(self, "自定义文件类型",
                                                   "请输入文件扩展名，用分号分隔：\n例如: .py;.java;.cpp",
                                                   text="")
            if not ok or not custom_types:
                self.exact_search_button.setEnabled(True)
                self.cancel_button.setEnabled(False)
                return
            file_types = [ext.strip().lower() for ext in custom_types.split(';') if ext.strip()]

        self.search_results = []
        self.results_tree.clear()
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.found_files_count = 0
        self.status_count_label.setText("已找到: 0 个文件")
        self.status_label.setText("正在执行精确搜索...")
        QApplication.processEvents()

        size_range = self.file_size_combo.currentData()
        mod_date_range = self.mod_date_combo.currentData()

        keyword_results = {kw: [] for kw in keywords}
        all_found_files = {}

        # 执行精确搜索
        for folder in self.search_folders:
            if self.cancel_search:
                break

            folder_path = Path(folder)
            if not folder_path.exists():
                continue

            if include_subfolders:
                walk_iter = os.walk(folder)
            else:
                try:
                    files = [f for f in folder_path.iterdir() if f.is_file()]
                    walk_iter = [(str(folder_path), [], [f.name for f in files])]
                except Exception as e:
                    print(f"访问文件夹出错: {folder} - {str(e)}")
                    continue

            for root, _, files in walk_iter:
                if self.cancel_search:
                    break

                self.current_path_label.setText(f"当前搜索路径: {root}")
                self.status_label.setText(f"正在搜索: {root}")
                QApplication.processEvents()

                for file in files:
                    if self.cancel_search:
                        break

                    file_path = Path(root) / file

                    try:
                        if not file_path.exists() or not os.access(str(file_path), os.R_OK):
                            continue

                        file_stat = file_path.stat()
                        file_size = file_stat.st_size
                        mod_date = datetime.datetime.fromtimestamp(file_stat.st_mtime).date()

                        # 检查文件大小
                        if not (size_range[0] <= file_size <= size_range[1]):
                            continue

                        # 检查修改日期
                        if mod_date_range != (None, None) and mod_date_range != "custom":
                            start_date, end_date = mod_date_range
                            if not (start_date <= mod_date <= end_date):
                                continue

                        # 检查文件类型
                        ext = file_path.suffix.lower()
                        if file_types and ext not in file_types:
                            continue

                        # 精确关键词匹配 - 只在文件名中进行，且必须严格匹配
                        for keyword in keywords:
                            if exact_match_filename(file, keyword):
                                file_info = get_file_info_dict(file_path, file_size, mod_date)
                                keyword_results[keyword].append(file_info)
                                if str(file_path) not in all_found_files:
                                    all_found_files[str(file_path)] = file_info

                    except Exception as e:
                        print(f"跳过文件 {file_path}，原因: {str(e)}")
                        continue
        
        # 显示搜索结果
        self._display_search_results(all_found_files, keyword_results)

    def select_target_folder(self):
        """选择目标文件夹"""
        folder = QFileDialog.getExistingDirectory(self, "选择目标文件夹")
        if folder:
            self.target_folder = folder
            self.status_label.setText(f"目标文件夹已设置为: {folder}")
            self.copy_button.setEnabled(True)
            self.add_log(f"设置目标文件夹: {folder}", folder)

    # =============== 搜索执行 ===============
    
    def start_search(self):
        """开始搜索"""
        if not self.search_folders:
            QMessageBox.warning(self, "错误", "请添加至少一个搜索文件夹或盘符！")
            return

        self.cancel_button.setEnabled(True)
        self.cancel_search = False

        keywords_text = self.keyword_entry.toPlainText().strip()
        keywords = [kw.strip() for kw in re.split(r'[\s\n]+', keywords_text) if kw.strip()]

        if not keywords:
            QMessageBox.warning(self, "提示", "请输入至少一个关键词。")
            self.search_button.setEnabled(True)
            self.cancel_button.setEnabled(False)
            return

        file_types = self.filetype_combo.currentData()
        include_subfolders = self.subfolders_check.isChecked()
        search_mode = self.get_search_mode()

        self.add_log(f"开始搜索，关键词: {', '.join(keywords)}，文件类型: {self.filetype_combo.currentText()}")

        if file_types == "custom":
            custom_types, ok = QInputDialog.getText(self, "自定义文件类型",
                                                   "请输入文件扩展名，用分号分隔：\n例如: .py;.java;.cpp",
                                                   text="")
            if not ok or not custom_types:
                self.search_button.setEnabled(True)
                self.cancel_button.setEnabled(False)
                return
            file_types = [ext.strip().lower() for ext in custom_types.split(';') if ext.strip()]

        self.search_results = []
        self.results_tree.clear()
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.found_files_count = 0
        self.status_count_label.setText("已找到: 0 个文件")
        self.status_label.setText("正在搜索文件...")
        QApplication.processEvents()

        size_range = self.file_size_combo.currentData()
        mod_date_range = self.mod_date_combo.currentData()

        keyword_results = {kw: [] for kw in keywords}
        all_found_files = {}

        # 执行搜索
        for folder in self.search_folders:
            if self.cancel_search:
                break

            folder_path = Path(folder)
            if not folder_path.exists():
                continue

            if include_subfolders:
                walk_iter = os.walk(folder)
            else:
                try:
                    files = [f for f in folder_path.iterdir() if f.is_file()]
                    walk_iter = [(str(folder_path), [], [f.name for f in files])]
                except Exception as e:
                    print(f"访问文件夹出错: {folder} - {str(e)}")
                    continue

            for root, _, files in walk_iter:
                if self.cancel_search:
                    break

                self.current_path_label.setText(f"当前搜索路径: {root}")
                self.status_label.setText(f"正在搜索: {root}")
                QApplication.processEvents()

                for file in files:
                    if self.cancel_search:
                        break

                    file_path = Path(root) / file

                    try:
                        if not file_path.exists() or not os.access(str(file_path), os.R_OK):
                            continue

                        file_stat = file_path.stat()
                        file_size = file_stat.st_size
                        mod_date = datetime.datetime.fromtimestamp(file_stat.st_mtime).date()

                        # 检查文件大小
                        if not (size_range[0] <= file_size <= size_range[1]):
                            continue

                        # 检查修改日期
                        if mod_date_range != (None, None) and mod_date_range != "custom":
                            start_date, end_date = mod_date_range
                            if not (start_date <= mod_date <= end_date):
                                continue

                        # 检查文件类型
                        ext = file_path.suffix.lower()
                        if file_types and ext not in file_types:
                            continue

                        # 关键词匹配
                        for keyword in keywords:
                            filename_match = False
                            content_match = False

                            if search_mode in ["filename", "both"]:
                                filename_match = matches_keyword(file, keyword)

                            if search_mode in ["content", "both"] and not filename_match:
                                content_match = search_content(str(file_path), keyword)

                            if (search_mode == "filename" and filename_match) or \
                               (search_mode == "content" and content_match) or \
                               (search_mode == "both" and (filename_match or content_match)):

                                file_info = get_file_info_dict(file_path, file_size, mod_date)
                                keyword_results[keyword].append(file_info)
                                if str(file_path) not in all_found_files:
                                    all_found_files[str(file_path)] = file_info

                    except Exception as e:
                        print(f"跳过文件 {file_path}，原因: {str(e)}")
                        continue
        
        # 显示搜索结果
        self._display_search_results(all_found_files, keyword_results)

    def _display_search_results(self, all_found_files, keyword_results):
        """显示搜索结果"""
        self.search_results = list(all_found_files.values())
        self.results_tree.clear()
        
        # 建立文件路径到关键词的映射
        file_to_keywords = {}
        for keyword, files in keyword_results.items():
            for file_info in files:
                file_path = str(file_info['path'])
                if file_path not in file_to_keywords:
                    file_to_keywords[file_path] = []
                file_to_keywords[file_path].append(keyword)
        
        # 显示结果，并在第5列显示匹配的关键词
        for file_info in self.search_results:
            file_path = str(file_info['path'])
            matched_keywords = file_to_keywords.get(file_path, [])
            keywords_str = ", ".join(matched_keywords) if matched_keywords else "-"
            
            item = QTreeWidgetItem([
                file_info['name'],
                str(Path(file_info['path']).parent),
                format_size(file_info['size']),
                file_info['mod_date'],
                keywords_str
            ])
            item.setData(0, Qt.UserRole, file_info['path'])
            item.setToolTip(0, file_info['name'])
            item.setToolTip(1, str(Path(file_info['path']).parent))
            item.setToolTip(4, f"匹配关键词: {keywords_str}")
            self.results_tree.addTopLevelItem(item)

        # 存储keyword_results以供查看按钮使用
        self.keyword_results = keyword_results
        
        # 分类关键词：零结果、多结果
        zero_result_keywords = []  # 没有搜索到的关键词
        multi_result_keywords_info = []  # 搜索到多个的关键词及其对应的文件数
        
        for keyword in sorted(keyword_results.keys()):
            count = len(keyword_results[keyword])
            if count == 0:
                zero_result_keywords.append(keyword)
            elif count > 1:
                multi_result_keywords_info.append((keyword, count))
        
        # 存储未找到结果的关键词
        self.unfound_keywords = zero_result_keywords
        
        # 构建关键词统计文本（只显示有多个结果的）
        keywords_parts = []
        for keyword, count in multi_result_keywords_info:
            keywords_parts.append(f"{keyword}({count})")
        
        if keywords_parts:
            keywords_summary = "关键词统计: " + "  |  ".join(keywords_parts)
        else:
            keywords_summary = "未执行搜索"
        
        self.keywords_info_label.setText(keywords_summary)
        
        # 更新未找到结果的关键词区域
        self._update_unfound_keywords_display(zero_result_keywords)
        
        # 如果有多结果关键词，显示提示信息
        if multi_result_keywords_info:
            tooltip_text = "点击下方按钮查看具体结果: " + ", ".join([f"{kw}({count})" for kw, count in multi_result_keywords_info])
            self.keywords_info_label.setToolTip(tooltip_text)

        self.found_files_count = len(self.search_results)
        self.status_count_label.setText(f"已找到: {self.found_files_count} 个文件")
        
        self.progress_bar.setVisible(False)
        self.current_path_label.setText("当前搜索路径: ")

        if self.cancel_search:
            self.status_label.setText(f"搜索已取消，已找到 {self.found_files_count} 个文件")
            self.add_log("搜索已取消")
        else:
            self.status_label.setText(f"搜索完成，找到 {self.found_files_count} 个文件")
            self.add_log(f"搜索完成，找到 {self.found_files_count} 个文件")

        self.copy_button.setEnabled(bool(self.search_results))
        self.search_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        
        # 创建多结果关键词的查看按钮
        self._create_keyword_view_buttons(multi_result_keywords_info)
    
    def _update_unfound_keywords_display(self, unfound_keywords):
        """更新未找到结果的关键词显示区域"""
        if unfound_keywords:
            text = "\n".join(unfound_keywords)
            self.unfound_keywords_text.setPlainText(text)
            self.unfound_keywords_group.setVisible(True)
        else:
            self.unfound_keywords_text.setPlainText("")
            self.unfound_keywords_group.setVisible(False)

    def _create_keyword_view_buttons(self, multi_result_keywords_info):
        """为多结果关键词创建查看按钮"""
        # 清空现有按钮
        while self.keywords_buttons_container.layout().count():
            child = self.keywords_buttons_container.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # 为每个多结果关键词创建按钮
        for keyword, count in multi_result_keywords_info:
            button = QPushButton(f"查看: {keyword}({count})")
            button.setMaximumWidth(150)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 3px;
                    padding: 4px 8px;
                    font-size: 9pt;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            # 使用lambda保存keyword值
            button.clicked.connect(lambda checked, kw=keyword: self._show_keyword_results(kw))
            self.keywords_buttons_container.layout().addWidget(button)
        
        # 添加伸缩空间
        self.keywords_buttons_container.layout().addStretch()
    
    def _show_keyword_results(self, keyword):
        """显示指定关键词的所有查询结果"""
        if keyword not in self.keyword_results:
            return
        
        files = self.keyword_results[keyword]
        
        # 创建对话框
        dialog = QDialog(self)
        dialog.setWindowTitle(f"查询结果: {keyword}")
        dialog.setGeometry(300, 300, 700, 400)
        
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel(f"<b>关键词 '{keyword}' 的查询结果 ({len(files)} 个文件):</b>")
        layout.addWidget(title_label)
        
        # 结果树
        results_tree = QTreeWidget()
        results_tree.setHeaderLabels(["文件名", "路径", "大小", "修改时间"])
        results_tree.setColumnWidth(0, 200)
        results_tree.setColumnWidth(1, 250)
        results_tree.setColumnWidth(2, 80)
        results_tree.setColumnWidth(3, 120)
        
        for file_info in files:
            item = QTreeWidgetItem([
                file_info['name'],
                str(file_info['path']),
                format_size(file_info['size']),
                file_info['mod_date']
            ])
            results_tree.addTopLevelItem(item)
        
        layout.addWidget(results_tree)
        
        # 按钮
        button_layout = QHBoxLayout()
        close_button = QPushButton("关闭")
        close_button.clicked.connect(dialog.accept)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()

    # =============== 文件操作 ===============
    
    def copy_files(self):
        """复制文件"""
        if not self.target_folder:
            QMessageBox.warning(self, "错误", "请先选择目标文件夹！")
            return

        if not self.search_results:
            QMessageBox.warning(self, "错误", "没有可复制的文件！")
            return

        # 检查目标文件夹权限
        target_path = Path(self.target_folder)
        if not target_path.exists() or not os.access(str(target_path), os.W_OK):
            QMessageBox.critical(self, "错误", "目标文件夹无写入权限！")
            return

        target_path.mkdir(parents=True, exist_ok=True)

        # 检查冲突文件
        existing_files = set()
        for file_info in self.search_results:
            target_file = target_path / file_info['name']
            if target_file.exists():
                existing_files.add(file_info['name'])

        if not existing_files:
            copy_files_without_conflicts(self, self.search_results)
            return

        # 处理冲突
        conflict_dialog = FileConflictDialog(self, self.search_results, self.target_folder)
        if conflict_dialog.exec_() == FileConflictDialog.Accepted:
            files_to_copy = conflict_dialog.get_selected_files()
            copy_selected_files(self, files_to_copy)

    def delete_files(self):
        """删除文件"""
        if not self.search_results:
            QMessageBox.warning(self, "错误", "没有可删除的文件！")
            return

        # 显示免责声明
        disclaimer = (
            "您即将删除原文件，请谨慎操作\n\n"
            "【免责声明】本软件为免费工具，用户自愿使用。开发者不承诺软件绝对安全，"
            "对因使用软件导致的数据丢失、系统损坏等后果不承担责任。"
            "禁止将软件用于非法目的。"
        )
        reply = QMessageBox.warning(self, "警告", disclaimer,
                                  QMessageBox.Ok | QMessageBox.Cancel)

        if reply != QMessageBox.Ok:
            return

        # 二次确认
        reply = QMessageBox.question(self, "确认删除",
                                    "确定要永久删除原文件吗？此操作不可撤销！",
                                    QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            files_to_delete = [f['path'] for f in self.search_results]
            success_count, error_files = delete_files_batch(self, files_to_delete)

            if error_files:
                error_msg = "以下文件删除失败：\n\n" + "\n".join(error_files[:10])
                if len(error_files) > 10:
                    error_msg += f"\n\n...以及另外 {len(error_files)-10} 个文件"
                QMessageBox.warning(self, "删除错误",
                                   f"{error_msg}\n\n请手动删除这些文件。")

            self.status_label.setText(f"已删除 {success_count}/{len(self.search_results)} 个文件")
            
            # 更新结果树
            remaining_files = []
            for file_info in self.search_results:
                if Path(file_info['path']).exists():
                    remaining_files.append(file_info)
                else:
                    # 从树中移除
                    for index in range(self.results_tree.topLevelItemCount()):
                        item = self.results_tree.topLevelItem(index)
                        if item.data(0, Qt.UserRole) == file_info['path']:
                            self.results_tree.takeTopLevelItem(index)
                            break
            
            self.search_results = remaining_files
            self.delete_button.setEnabled(bool(self.search_results))

    def generate_pdf_log(self):
        """生成PDF日志"""
        file_path, _ = QFileDialog.getSaveFileName(self, "保存PDF日志", "", "PDF文件 (*.pdf)")
        if not file_path:
            return

        file_path = Path(file_path)
        if file_path.suffix.lower() != ".pdf":
            file_path = file_path.with_suffix(".pdf")

        if PDFLogGenerator.generate_pdf_log(self, str(file_path)):
            self.status_label.setText(f"PDF日志已保存到: {file_path}")
            self.add_log(f"生成PDF日志: {file_path}")
            QMessageBox.information(self, "成功", "PDF日志已成功生成！")

    # =============== 右键菜单和其他交互 ===============
    
    def show_context_menu(self, position):
        """显示右键菜单"""
        menu = QMenu()
        open_file_action = QAction("打开文件", self)
        open_file_action.triggered.connect(self.open_selected_file)
        open_folder_action = QAction("打开所在文件夹", self)
        open_folder_action.triggered.connect(self.open_file_folder)

        menu.addAction(open_file_action)
        menu.addAction(open_folder_action)
        menu.exec_(self.results_tree.viewport().mapToGlobal(position))

    def open_selected_file(self):
        """打开选中的文件"""
        selected_items = self.results_tree.selectedItems()
        if not selected_items:
            return

        file_path = selected_items[0].data(0, Qt.UserRole)
        try:
            os.startfile(file_path)
            self.add_log(f"打开文件: {file_path}", file_path)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"无法打开文件: {str(e)}")

    def open_file_folder(self):
        """打开文件所在文件夹"""
        selected_items = self.results_tree.selectedItems()
        if not selected_items:
            return

        file_path = selected_items[0].data(0, Qt.UserRole)
        folder_path = Path(file_path).parent

        try:
            os.startfile(str(folder_path))
            self.add_log(f"打开所在文件夹: {folder_path}", folder_path)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"无法打开文件夹: {str(e)}")

    def show_file_info(self, item, column):
        """显示文件详细信息"""
        file_path = item.data(0, Qt.UserRole)
        if not file_path:
            return

        file_path = Path(file_path)
        try:
            file_stat = file_path.stat()
            size = format_size(file_stat.st_size)
            mod_date = datetime.datetime.fromtimestamp(file_stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            create_date = datetime.datetime.fromtimestamp(file_stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")

            owner = "未知"
            try:
                import win32security
                sd = win32security.GetFileSecurity(str(file_path), win32security.OWNER_SECURITY_INFORMATION)
                owner_sid = sd.GetSecurityDescriptorOwner()
                owner, _, _ = win32security.LookupAccountSid(None, owner_sid)
            except:
                pass

            content_preview = ""
            try:
                encodings = ['utf-8', 'gbk', 'latin-1']
                for encoding in encodings:
                    try:
                        with file_path.open('r', encoding=encoding, errors='ignore') as f:
                            content_preview = f.read(300)
                            break
                    except UnicodeDecodeError:
                        continue
            except:
                content_preview = "无法预览文件内容"

            file_status = "状态: 可用"
            if is_file_locked(str(file_path)):
                file_status = "状态: <font color='red'>被其他程序占用</font>"

            info = f"""
            <b>文件信息</b>
            <table>
            <tr><td><b>文件名：</b></td><td>{file_path.name}</td></tr>
            <tr><td><b>路径：</b></td><td>{file_path}</td></tr>
            <tr><td><b>大小：</b></td><td>{size}</td></tr>
            <tr><td><b>修改日期：</b></td><td>{mod_date}</td></tr>
            <tr><td><b>创建日期：</b></td><td>{create_date}</td></tr>
            <tr><td><b>所有者：</b></td><td>{owner}</td></tr>
            <tr><td><b>{file_status}</b></td><td></td></tr>
            </table>
            <b>内容预览 (前300字符)：</b>
            <pre>{content_preview}</pre>
            """

            QMessageBox.information(self, "文件详情", info)
            self.add_log(f"查看文件信息: {file_path}", file_path)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"无法获取文件信息: {str(e)}")

    def show_help(self):
        """显示帮助信息"""
        help_text = f"""
        <div style="color: red; font-weight: bold; border: 1px solid red; padding: 10px; margin-bottom: 20px;">
        【免责声明】本软件为免费工具，用户自愿使用。开发者不承诺软件绝对安全，
        对因使用软件导致的数据丢失、系统损坏等后果不承担责任。
        禁止将软件用于非法目的。
        </div>
        
        <h2>文件归集管理器 V{self.version} 使用说明</h2>
        
        <h3>基本功能</h3>
        <p>文件归集管理器是一个强大的文件集中管理工具，可以帮助您搜索、整理和管理计算机中的文件。</p>
        
        <h3>操作步骤</h3>
        <ol>
            <li><b>添加搜索文件夹/盘符</b>：使用"添加文件夹"或"添加盘符"按钮选择搜索范围</li>
            <li><b>设置搜索条件</b>： 
                <ul>
                    <li>关键词：支持高级搜索语法（将鼠标悬停在输入框上查看详情）</li>
                    <li>搜索模式：选择文件名/内容/两者同时搜索</li>
                    <li>文件类型：按类别筛选文件（将鼠标悬停在选择框上查看详情）</li>
                    <li>修改日期：按时间范围筛选文件（将鼠标悬停在选择框上查看详情）</li>
                    <li>文件大小：按大小范围筛选文件（将鼠标悬停在选择框上查看详情）</li>
                </ul>
            </li>
            <li><b>开始搜索</b>：点击"开始搜索"按钮执行搜索</li>
            <li><b>选择目标文件夹</b>：点击"选择目标位置"按钮指定文件复制位置</li>
            <li><b>复制文件</b>：点击"开始文件归集"按钮复制文件</li>
            <li><b>删除原文件：可选步骤，永久删除原文件（不可撤销）</b></li>
            <li><b>生成PDF日志</b>：创建操作记录PDF文件</li>
        </ol>
        
        <h3>高级功能</h3>
        <ul>
            <li><b>搜索模式选择</b>：灵活选择仅文件名/仅内容/两者同时搜索</li>
            <li><b>多文件夹搜索</b>：支持同时搜索多个文件夹或整个盘符</li>
            <li><b>右键菜单</b>：在搜索结果上右键可打开文件或所在文件夹</li>
            <li><b>冲突处理</b>：自动检测目标文件夹中的同名文件并提供解决方案</li>
            <li><b>多语言支持</b>：PDF日志支持中文、英文、日文等多种语言</li>
            <li><b>文件占用检测</b>：自动检测并提示被占用的文件</li>
            <li><b>搜索状态显示</b>：实时显示当前搜索的文件夹路径</li>
        </ul>
        
        <h3>版本更新记录</h3>
        <p><b>V2.3.5 (2025-11-29)</b></p>
        <ul>
            <li>完成代码重构，改进易读性和组织性</li>
            <li>将应用程序拆分为多个组件模块</li>
            <li>提高代码可维护性和扩展性</li>
        </ul>
        <p><b>V2.3.4 (2025-07-17)</b></p>
        <ul>
            <li>优化搜索结果及按钮显示</li>
        </ul>
        """

        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("使用说明")
        help_dialog.setGeometry(200, 200, 700, 600)

        layout = QVBoxLayout()

        text_edit = QLabel(help_text)
        text_edit.setWordWrap(True)

        scroll_area = QScrollArea()
        scroll_area.setWidget(text_edit)
        scroll_area.setWidgetResizable(True)

        layout.addWidget(scroll_area)

        close_button = QPushButton("关闭")
        close_button.clicked.connect(help_dialog.accept)
        layout.addWidget(close_button, alignment=Qt.AlignCenter)

        help_dialog.setLayout(layout)
        help_dialog.exec_()
