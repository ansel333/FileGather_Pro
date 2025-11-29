"""
Search Operations - Handles all search-related operations
Contains methods for folder search, exact search, and main search functionality
"""

import os
import datetime
import re
from pathlib import Path

from PyQt5.QtWidgets import QMessageBox, QInputDialog, QApplication

from ..search_logic import matches_keyword, search_content, exact_match_filename
from ..utils import get_file_info_dict


def start_search(self):
    """开始搜索"""
    if not self.search_folders:
        QMessageBox.warning(self, "错误", "请添加至少一个搜索文件夹或盘符！")
        return

    self.cancel_button.setEnabled(True)
    self.cancel_search = False

    # 检查聚合模式
    gather_mode = self.gather_mode_combo.currentData()
    
    # 如果是文件夹归集模式，使用不同的搜索逻辑
    if gather_mode == "folder":
        self._start_folder_search()
        return

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


def start_exact_search(self):
    """开始精确搜索 - 文件名必须严格匹配"""
    if not self.search_folders:
        QMessageBox.warning(self, "错误", "请添加至少一个搜索文件夹或盘符！")
        return

    self.cancel_button.setEnabled(True)
    self.cancel_search = False

    # 检查聚合模式
    gather_mode = self.gather_mode_combo.currentData()
    
    # 如果是文件夹归集模式，使用不同的搜索逻辑
    if gather_mode == "folder":
        self._start_folder_exact_search()
        return

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


def search_folders_by_name(self):
    """文件夹名称搜索 - 仅搜索第一级子文件夹"""
    keywords_text = self.keyword_entry.toPlainText().strip()
    keywords = [kw.strip() for kw in re.split(r'[\s\n]+', keywords_text) if kw.strip()]

    if not keywords:
        QMessageBox.warning(self, "提示", "请输入至少一个关键词。")
        return None

    keyword_results = {kw: [] for kw in keywords}
    all_found_folders = {}

    for folder in self.search_folders:
        if self.cancel_search:
            break

        folder_path = Path(folder)
        if not folder_path.exists():
            continue

        try:
            # 仅搜索第一级子文件夹
            subdirs = [d for d in folder_path.iterdir() if d.is_dir()]
        except Exception as e:
            print(f"访问文件夹出错: {folder} - {str(e)}")
            continue

        for subdir in subdirs:
            if self.cancel_search:
                break

            dir_name = subdir.name

            # 关键词匹配
            search_mode = self.get_search_mode()
            for keyword in keywords:
                matches = False

                if search_mode in ["filename", "both"]:
                    matches = matches_keyword(dir_name, keyword)

                if matches:
                    # 获取文件夹信息
                    try:
                        dir_stat = subdir.stat()
                        mod_date = datetime.datetime.fromtimestamp(dir_stat.st_mtime).date()
                        
                        folder_info = {
                            "path": str(subdir),
                            "name": dir_name,
                            "size": 0,  # 文件夹不计算大小
                            "date": mod_date.strftime("%Y-%m-%d")
                        }

                        keyword_results[keyword].append(folder_info)
                        if str(subdir) not in all_found_folders:
                            all_found_folders[str(subdir)] = folder_info
                    except Exception as e:
                        print(f"获取文件夹信息失败: {subdir} - {str(e)}")
                        continue

    return all_found_folders, keyword_results


def _start_folder_search(self):
    """文件夹归集模式 - 开始搜索"""
    keywords_text = self.keyword_entry.toPlainText().strip()
    keywords = [kw.strip() for kw in re.split(r'[\s\n]+', keywords_text) if kw.strip()]

    if not keywords:
        QMessageBox.warning(self, "提示", "请输入至少一个关键词。")
        self.search_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        return

    self.add_log(f"开始搜索文件夹，关键词: {', '.join(keywords)}")

    self.search_results = []
    self.results_tree.clear()
    self.progress_bar.setVisible(True)
    self.progress_bar.setValue(0)
    self.found_files_count = 0
    self.status_count_label.setText("已找到: 0 个文件夹")
    self.status_label.setText("正在搜索文件夹...")
    QApplication.processEvents()

    search_mode = self.get_search_mode()
    keyword_results = {kw: [] for kw in keywords}
    all_found_folders = {}

    # 执行文件夹搜索
    for folder in self.search_folders:
        if self.cancel_search:
            break

        folder_path = Path(folder)
        if not folder_path.exists():
            continue

        try:
            # 仅搜索第一级子文件夹
            subdirs = [d for d in folder_path.iterdir() if d.is_dir()]
        except Exception as e:
            print(f"访问文件夹出错: {folder} - {str(e)}")
            continue

        self.current_path_label.setText(f"当前搜索路径: {folder}")
        self.status_label.setText(f"正在搜索: {folder}")
        QApplication.processEvents()

        for subdir in subdirs:
            if self.cancel_search:
                break

            dir_name = subdir.name

            # 关键词匹配
            for keyword in keywords:
                matches = False

                if search_mode in ["filename", "both"]:
                    matches = matches_keyword(dir_name, keyword)

                if matches:
                    # 获取文件夹信息
                    try:
                        dir_stat = subdir.stat()
                        mod_date = datetime.datetime.fromtimestamp(dir_stat.st_mtime).date()
                        
                        folder_info = {
                            "path": str(subdir),
                            "name": dir_name,
                            "size": 0,
                            "mod_date": mod_date.strftime("%Y-%m-%d")
                        }

                        keyword_results[keyword].append(folder_info)
                        if str(subdir) not in all_found_folders:
                            all_found_folders[str(subdir)] = folder_info
                            self.found_files_count += 1
                            self.status_count_label.setText(f"已找到: {self.found_files_count} 个文件夹")
                    except Exception as e:
                        print(f"获取文件夹信息失败: {subdir} - {str(e)}")
                        continue

    # 显示搜索结果
    self._display_search_results(all_found_folders, keyword_results)


def _start_folder_exact_search(self):
    """文件夹归集模式 - 精确搜索"""
    keywords_text = self.keyword_entry.toPlainText().strip()
    keywords = [kw.strip() for kw in re.split(r'[\s\n]+', keywords_text) if kw.strip()]

    if not keywords:
        QMessageBox.warning(self, "提示", "请输入至少一个关键词。")
        self.exact_search_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        return

    self.add_log(f"开始精确搜索文件夹，关键词: {', '.join(keywords)}")

    self.search_results = []
    self.results_tree.clear()
    self.progress_bar.setVisible(True)
    self.progress_bar.setValue(0)
    self.found_files_count = 0
    self.status_count_label.setText("已找到: 0 个文件夹")
    self.status_label.setText("正在执行精确搜索...")
    QApplication.processEvents()

    keyword_results = {kw: [] for kw in keywords}
    all_found_folders = {}

    # 执行文件夹精确搜索
    for folder in self.search_folders:
        if self.cancel_search:
            break

        folder_path = Path(folder)
        if not folder_path.exists():
            continue

        try:
            # 仅搜索第一级子文件夹
            subdirs = [d for d in folder_path.iterdir() if d.is_dir()]
        except Exception as e:
            print(f"访问文件夹出错: {folder} - {str(e)}")
            continue

        self.current_path_label.setText(f"当前搜索路径: {folder}")
        self.status_label.setText(f"正在搜索: {folder}")
        QApplication.processEvents()

        for subdir in subdirs:
            if self.cancel_search:
                break

            dir_name = subdir.name

            # 精确关键词匹配
            for keyword in keywords:
                if exact_match_filename(dir_name, keyword):
                    # 获取文件夹信息
                    try:
                        dir_stat = subdir.stat()
                        mod_date = datetime.datetime.fromtimestamp(dir_stat.st_mtime).date()
                        
                        folder_info = {
                            "path": str(subdir),
                            "name": dir_name,
                            "size": 0,
                            "mod_date": mod_date.strftime("%Y-%m-%d")
                        }

                        keyword_results[keyword].append(folder_info)
                        if str(subdir) not in all_found_folders:
                            all_found_folders[str(subdir)] = folder_info
                            self.found_files_count += 1
                            self.status_count_label.setText(f"已找到: {self.found_files_count} 个文件夹")
                    except Exception as e:
                        print(f"获取文件夹信息失败: {subdir} - {str(e)}")
                        continue

    # 显示搜索结果
    self._display_search_results(all_found_folders, keyword_results)
