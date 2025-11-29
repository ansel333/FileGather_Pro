"""
Folder Manager - Handles folder selection and management
"""

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QMenu, QAction
from pathlib import Path


def add_search_folder(self):
    """添加搜索文件夹"""
    folder = QFileDialog.getExistingDirectory(self, "选择搜索文件夹")
    if folder and folder not in self.search_folders:
        self.search_folders.append(folder)
        update_folder_list(self)
        self.add_log(f"添加搜索文件夹: {folder}", folder)


def add_drive(self):
    """添加盘符"""
    drives = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if Path(f"{d}:").exists()]
    if not drives:
        QMessageBox.information(self, "信息", "未找到可用盘符")
        return

    menu = QMenu(self)
    for drive in drives:
        action = QAction(drive, self)
        action.triggered.connect(lambda checked, d=drive: add_drive_action(self, d))
        menu.addAction(action)

    pos = self.add_drive_button.mapToGlobal(QPoint(0, self.add_drive_button.height()))
    menu.exec_(pos)


def add_drive_action(self, drive):
    """添加盘符到搜索列表"""
    if drive not in self.search_folders:
        self.search_folders.append(drive)
        update_folder_list(self)
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

    update_folder_list(self)


def clear_search_folders(self):
    """清空所有搜索文件夹"""
    self.search_folders = []
    update_folder_list(self)
    self.add_log("清空搜索文件夹列表")


def update_folder_list(self):
    """更新文件夹列表显示"""
    self.folder_list.clear()
    for folder in self.search_folders:
        self.folder_list.addItem(folder)
