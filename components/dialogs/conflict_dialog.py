"""
文件冲突处理对话框模块
处理复制文件时的覆盖、跳过、重命名等冲突解决方案
"""

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QAbstractItemView, QPushButton, QMessageBox, QDialogButtonBox
)


class FileConflictDialog(QDialog):
    """文件冲突处理对话框"""
    
    def __init__(self, parent, files, target_folder):
        """
        初始化文件冲突对话框
        
        Args:
            parent: 父窗口
            files: 文件列表，每个文件是字典类型
            target_folder: 目标文件夹路径
        """
        super().__init__(parent)
        self.setWindowTitle("处理文件冲突")
        self.setGeometry(300, 300, 800, 500)

        self.files = files
        self.target_folder = target_folder
        self.selected_files = []

        self._init_ui()

    def _init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout()

        # 标题
        title = QLabel("<b>检测到目标文件夹中存在同名文件，请选择处理方式：</b>")
        layout.addWidget(title)

        # 文件列表
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QAbstractItemView.ExtendedSelection)

        for file_info in self.files:
            file_name = file_info['name']
            target_path = Path(self.target_folder) / file_name

            conflict = "存在冲突" if target_path.exists() else ""

            item = QListWidgetItem(f"{file_name} - {conflict}")
            item.setData(Qt.UserRole, file_info)
            self.file_list.addItem(item)

            if conflict:
                item.setForeground(QColor("red"))

        layout.addWidget(self.file_list)

        # 帮助提示
        help_label = QLabel("提示: 选择文件后点击下方按钮设置处理方式")
        help_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout.addWidget(help_label)

        # 操作按钮
        button_layout = QHBoxLayout()

        self.overwrite_button = QPushButton("覆盖")
        self.overwrite_button.setToolTip("替换目标文件夹中的文件")
        self.overwrite_button.clicked.connect(lambda: self.set_action("overwrite"))

        self.skip_button = QPushButton("跳过")
        self.skip_button.setToolTip("不复制此文件")
        self.skip_button.clicked.connect(lambda: self.set_action("skip"))

        self.rename_button = QPushButton("重命名")
        self.rename_button.setToolTip("复制文件并重命名")
        self.rename_button.clicked.connect(lambda: self.set_action("rename"))

        self.auto_rename_button = QPushButton("全部重命名")
        self.auto_rename_button.setToolTip("为所有冲突文件添加后缀")
        self.auto_rename_button.clicked.connect(self.auto_rename_all)

        self.overwrite_all_button = QPushButton("全部覆盖")
        self.overwrite_all_button.setToolTip("将所有冲突文件全部覆盖")
        self.overwrite_all_button.clicked.connect(self.overwrite_all)

        button_layout.addWidget(self.overwrite_button)
        button_layout.addWidget(self.skip_button)
        button_layout.addWidget(self.rename_button)
        button_layout.addWidget(self.auto_rename_button)
        button_layout.addWidget(self.overwrite_all_button)

        layout.addLayout(button_layout)

        # 确定/取消按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)

        self.setLayout(layout)

    def set_action(self, action):
        """为选中的文件设置操作类型"""
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "请先选择文件！")
            return

        for item in selected_items:
            file_info = item.data(Qt.UserRole)

            if action == "overwrite":
                item.setText(f"{file_info['name']} - 将覆盖")
                item.setForeground(QColor("blue"))
                file_info['action'] = "overwrite"
                file_info['new_name'] = file_info['name']
            
            elif action == "skip":
                item.setText(f"{file_info['name']} - 将跳过")
                item.setForeground(QColor("gray"))
                file_info['action'] = "skip"
            
            elif action == "rename":
                new_name = self._generate_unique_name(file_info['name'])
                item.setText(f"{file_info['name']} -> {new_name}")
                file_info['action'] = "rename"
                file_info['new_name'] = new_name
                item.setForeground(QColor("darkgreen"))

    def auto_rename_all(self):
        """为所有冲突文件自动重命名"""
        for index in range(self.file_list.count()):
            item = self.file_list.item(index)
            file_info = item.data(Qt.UserRole)

            if "存在冲突" in item.text():
                new_name = self._generate_unique_name(file_info['name'])
                item.setText(f"{file_info['name']} -> {new_name}")
                file_info['action'] = "rename"
                file_info['new_name'] = new_name
                item.setForeground(QColor("darkgreen"))

    def overwrite_all(self):
        """将所有冲突文件设置为覆盖"""
        for index in range(self.file_list.count()):
            item = self.file_list.item(index)
            file_info = item.data(Qt.UserRole)
            item.setText(f"{file_info['name']} - 将覆盖")
            item.setForeground(QColor("blue"))
            file_info['action'] = "overwrite"
            file_info['new_name'] = file_info['name']

    def get_selected_files(self):
        """获取处理后的文件列表"""
        result = []
        for file_info in self.files:
            action = file_info.get('action', 'overwrite')
            
            if action == "skip":
                continue
            
            if action == "rename":
                if 'new_name' not in file_info:
                    file_info['new_name'] = self._generate_unique_name(file_info['name'])
            else:
                file_info['new_name'] = file_info['name']
            
            result.append(file_info)
        
        return result

    def _generate_unique_name(self, original_name):
        """生成唯一的文件名"""
        file_path = Path(original_name)
        base = file_path.stem
        ext = file_path.suffix
        counter = 1
        new_name = f"{base}_{counter}{ext}"
        target_path = Path(self.target_folder) / new_name
        
        while target_path.exists():
            counter += 1
            new_name = f"{base}_{counter}{ext}"
            target_path = Path(self.target_folder) / new_name
        
        return new_name
