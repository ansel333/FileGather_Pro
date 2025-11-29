"""
搜索结果对话框模块
显示关键词搜索结果的树形视图
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTreeWidget, QTreeWidgetItem,
    QDialogButtonBox
)


class KeywordSearchResultDialog(QDialog):
    """关键词搜索结果对话框"""
    
    def __init__(self, parent, keyword_results):
        """
        初始化搜索结果对话框
        
        Args:
            parent: 父窗口
            keyword_results: 字典，格式为 {keyword: [file_info, ...]}
        """
        super().__init__(parent)
        self.setWindowTitle("关键词搜索结果")
        self.setGeometry(300, 300, 800, 500)

        layout = QVBoxLayout()

        title = QLabel("<b>每个关键词的搜索结果如下：</b>")
        layout.addWidget(title)

        # 创建结果树形视图
        self.results_tree = QTreeWidget()
        self.results_tree.setHeaderLabels(["关键词 / 文件名", "路径"])
        self.results_tree.setColumnWidth(0, 350)

        # 填充结果数据
        for keyword, files in keyword_results.items():
            keyword_item = QTreeWidgetItem([keyword])
            self.results_tree.addTopLevelItem(keyword_item)
            
            if files:
                for file_info in files:
                    file_item = QTreeWidgetItem([file_info['name'], file_info['path']])
                    keyword_item.addChild(file_item)
            else:
                # 如果没有找到文件，显示灰色提示
                no_result_item = QTreeWidgetItem(["未找到文件", ""])
                keyword_item.addChild(no_result_item)
                keyword_item.setForeground(0, QColor("gray"))

        self.results_tree.expandAll()
        layout.addWidget(self.results_tree)

        # 确定按钮
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)

        self.setLayout(layout)
