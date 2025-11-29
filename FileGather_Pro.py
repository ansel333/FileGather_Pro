"""
文件归集管理器 2.4.0
应用程序主入口文件

将应用程序重构为多个组件模块，改善了代码易读性和组织性
添加精确查找功能，支持文件名严格匹配
"""

import sys
import os
from PyQt5.QtWidgets import QApplication

# 添加components路径到模块搜索路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from components.main_window import FileGatherPro


def main():
    """应用程序主函数"""
    app = QApplication(sys.argv)
    window = FileGatherPro()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
