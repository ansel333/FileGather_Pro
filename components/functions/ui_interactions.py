"""
UI Interactions - Handles user interaction methods
Includes logging, file opening, help display, and other UI-related operations
"""

import os
import datetime
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMessageBox, QScrollArea, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDialog
)


def add_log(self, action, file_path=None):
    """添加操作日志"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    self.operation_log.append(f"{timestamp} - {action}")
    if file_path:
        self.operated_files.add(str(file_path))


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


def cancel_search_action(self):
    """取消搜索"""
    self.cancel_search = True
    self.status_label.setText("搜索已取消")
    self.cancel_button.setEnabled(False)
    self.search_button.setEnabled(True)
    self.exact_search_button.setEnabled(True)
    self.add_log("取消搜索")
