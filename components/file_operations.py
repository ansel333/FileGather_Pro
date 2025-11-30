"""
文件操作模块
处理文件复制、删除、冲突检测等操作
"""

import os
import shutil
import hashlib
from pathlib import Path
from PyQt6.QtWidgets import QMessageBox, QApplication


def calculate_hash(filepath):
    """计算文件的SHA256哈希值"""
    h = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        print(f"无法计算哈希值 {filepath}: {e}")
        return None


def copy_files_without_conflicts(parent, files_to_copy):
    """不存在冲突的文件复制"""
    if not files_to_copy:
        return

    parent.progress_bar.setVisible(True)
    parent.progress_bar.setValue(0)
    parent.status_label.setText("正在复制文件...")
    QApplication.processEvents()

    error_files = []

    for i, file_info in enumerate(files_to_copy):
        src = Path(file_info['path'])
        dst = Path(parent.target_folder) / file_info['name']

        try:
            shutil.copy2(str(src), str(dst))
            parent.add_log(f"复制文件到目标文件夹: {dst}", src)
        except Exception as e:
            error_files.append(f"{src} ({str(e)})")

        progress = int((i + 1) / len(files_to_copy) * 100)
        parent.progress_bar.setValue(progress)
        if i % 10 == 0:
            QApplication.processEvents()

    parent.progress_bar.setVisible(False)

    if error_files:
        error_msg = "以下文件复制失败：\n\n" + "\n".join(error_files[:10])
        if len(error_files) > 10:
            error_msg += f"\n\n...以及另外 {len(error_files)-10} 个文件"
        QMessageBox.warning(parent, "复制错误", error_msg)
        parent.status_label.setText(f"已成功复制 {len(files_to_copy)-len(error_files)} 个文件，{len(error_files)} 个失败")
    else:
        parent.status_label.setText(f"已成功复制 {len(files_to_copy)} 个文件到目标文件夹")
        parent.delete_button.setEnabled(True)


def copy_selected_files(parent, files_to_copy):
    """复制指定的文件（处理冲突后）"""
    parent.progress_bar.setVisible(True)
    parent.progress_bar.setValue(0)
    parent.status_label.setText("正在复制文件...")
    QApplication.processEvents()

    error_files = []

    for i, file_info in enumerate(files_to_copy):
        src = Path(file_info['path'])
        dst = Path(parent.target_folder) / file_info['new_name']

        try:
            shutil.copy2(str(src), str(dst))
            parent.add_log(f"复制文件到目标文件夹: {dst}", src)
        except Exception as e:
            error_files.append(f"{src} ({str(e)})")

        progress = int((i + 1) / len(files_to_copy) * 100)
        parent.progress_bar.setValue(progress)
        if i % 10 == 0:
            QApplication.processEvents()

    parent.progress_bar.setVisible(False)

    if error_files:
        error_msg = "以下文件复制失败：\n\n" + "\n".join(error_files[:10])
        if len(error_files) > 10:
            error_msg += f"\n\n...以及另外 {len(error_files)-10} 个文件"
        QMessageBox.warning(parent, "复制错误", error_msg)
        parent.status_label.setText(f"已成功复制 {len(files_to_copy)-len(error_files)} 个文件，{len(error_files)} 个失败")
    else:
        parent.status_label.setText(f"已成功复制 {len(files_to_copy)} 个文件到目标文件夹")
        parent.delete_button.setEnabled(True)


def delete_files_batch(parent, files_to_delete):
    """批量删除文件"""
    if not files_to_delete:
        return 0, []

    parent.progress_bar.setVisible(True)
    parent.progress_bar.setValue(0)
    parent.status_label.setText("正在删除文件...")
    QApplication.processEvents()

    success_count = 0
    error_files = []
    total_files = len(files_to_delete)
    update_interval = max(1, total_files // 50)

    for i, file_path in enumerate(files_to_delete):
        file_path = Path(file_path)
        try:
            if not file_path.exists():
                error_files.append(f"{file_path} (文件不存在)")
                continue

            # 如果是目录，使用 rmtree 删除；否则使用 unlink 删除
            if file_path.is_dir():
                shutil.rmtree(str(file_path))
            else:
                file_path.unlink()
            
            parent.add_log(f"删除文件: {file_path}", file_path)
            success_count += 1

        except Exception as e:
            error_files.append(f"{file_path} ({str(e)})")

        if i % update_interval == 0 or i == total_files - 1:
            progress = int((i + 1) / total_files * 100)
            parent.progress_bar.setValue(progress)
            QApplication.processEvents()

    parent.progress_bar.setVisible(False)
    return success_count, error_files


def copy_folders_without_conflicts(parent, folders_to_copy):
    """复制文件夹（不存在冲突）"""
    if not folders_to_copy:
        return

    parent.progress_bar.setVisible(True)
    parent.progress_bar.setValue(0)
    parent.status_label.setText("正在复制文件夹...")
    QApplication.processEvents()

    error_folders = []

    for i, folder_info in enumerate(folders_to_copy):
        src = Path(folder_info['path'])
        dst = Path(parent.target_folder) / folder_info['name']

        try:
            # 如果目标文件夹已存在，添加后缀
            if dst.exists():
                counter = 1
                dst = Path(parent.target_folder) / f"{folder_info['name']}_{counter}"
                while dst.exists():
                    counter += 1
                    dst = Path(parent.target_folder) / f"{folder_info['name']}_{counter}"
            
            shutil.copytree(str(src), str(dst))
            parent.add_log(f"复制文件夹到目标文件夹: {dst}", src)
        except Exception as e:
            error_folders.append(f"{src} ({str(e)})")

        progress = int((i + 1) / len(folders_to_copy) * 100)
        parent.progress_bar.setValue(progress)
        if i % 10 == 0:
            QApplication.processEvents()

    parent.progress_bar.setVisible(False)

    if error_folders:
        error_msg = "以下文件夹复制失败：\n\n" + "\n".join(error_folders[:10])
        if len(error_folders) > 10:
            error_msg += f"\n\n...以及另外 {len(error_folders)-10} 个文件夹"
        QMessageBox.warning(parent, "复制错误", error_msg)
        parent.status_label.setText(f"已成功复制 {len(folders_to_copy)-len(error_folders)} 个文件夹，{len(error_folders)} 个失败")
    else:
        parent.status_label.setText(f"已成功复制 {len(folders_to_copy)} 个文件夹到目标文件夹")
        parent.delete_button.setEnabled(True)
