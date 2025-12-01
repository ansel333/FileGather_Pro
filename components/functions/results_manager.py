"""
Results Manager - Handles search results display and management
Includes keyword view buttons, result display, and UI updates
"""

import datetime
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QTreeWidgetItem, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTreeWidget, QWidget, QApplication
)

from ..utils import format_size


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
        item.setData(0, Qt.ItemDataRole.UserRole, file_info['path'])
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
    """更新未找到结果的关键词显示区域 - 使用树形控件"""
    self.unfound_keywords = unfound_keywords
    
    self.unfound_keywords_tree.clear()
    
    if unfound_keywords:
        # 创建根节点
        root_item = QTreeWidgetItem([f"未找到结果的关键词 ({len(unfound_keywords)}项)"])
        root_item.setExpanded(True)
        self.unfound_keywords_tree.addTopLevelItem(root_item)
        
        # 为每个关键词添加子节点
        for keyword in unfound_keywords:
            child_item = QTreeWidgetItem([keyword])
            root_item.addChild(child_item)
        
        # 显示容器
        self.unfound_keywords_container.setVisible(True)
    else:
        self.unfound_keywords_tree.clear()
        self.unfound_keywords_container.setVisible(False)


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
    dialog.exec()


def show_context_menu(self, position):
    """昺示右键菜单"""
    from PyQt6.QtGui import QAction
    from PyQt6.QtWidgets import QMenu
    
    menu = QMenu()
    open_file_action = QAction("打开文件", self)
    open_file_action.triggered.connect(self.open_selected_file)
    open_folder_action = QAction("打开所在文件夹", self)
    open_folder_action.triggered.connect(self.open_file_folder)

    menu.addAction(open_file_action)
    menu.addAction(open_folder_action)
    menu.exec_(self.results_tree.viewport().mapToGlobal(position))


def show_file_info(self, item, column):
    """显示文件详细信息"""
    import os
    from PyQt6.QtWidgets import QMessageBox
    
    file_path = item.data(0, Qt.ItemDataRole.UserRole)
    if not file_path:
        return

    file_path = Path(file_path)
    try:
        from ..utils import is_file_locked
        
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
    except Exception as e:
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.warning(self, "错误", f"无法获取文件信息: {str(e)}")

def toggle_unfound_list(self):
    """切换未找到关键词树的显示/隐藏"""
    is_visible = self.unfound_keywords_tree.isVisible()
    self.unfound_keywords_tree.setVisible(not is_visible)


def copy_unfound_keywords(self):
    """复制所有未找到的关键词到剪贴板"""
    if self.unfound_keywords:
        text = "\n".join(self.unfound_keywords)
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        self.add_log(f"已复制 {len(self.unfound_keywords)} 个未找到的关键词到剪贴板")


def on_unfound_keyword_item_clicked(self, item, column):
    """处理树项点击事件 - 展开/折叠根节点"""
    # 根节点自动展开/折叠
    if item.parent() is None:
        item.setExpanded(not item.isExpanded())

