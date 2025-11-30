"""
File Operations UI - Handles file operations through UI interactions
Includes copy, delete, and PDF log generation
"""

import os
from pathlib import Path

from PyQt6.QtWidgets import QFileDialog, QMessageBox, QApplication

from ..file_operations import copy_files_without_conflicts, copy_selected_files, delete_files_batch
from ..dialogs import FileConflictDialog, PDFLogGenerator


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
        from PyQt6.QtCore import Qt
        
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


def select_target_folder(self):
    """选择目标文件夹"""
    folder = QFileDialog.getExistingDirectory(self, "选择目标文件夹")
    if folder:
        self.target_folder = folder
        self.status_label.setText(f"目标文件夹已设置为: {folder}")
        self.copy_button.setEnabled(True)
        self.add_log(f"设置目标文件夹: {folder}", folder)
