"""
文件归集管理器
应用程序主入口文件

将应用程序重构为多个组件模块，改善了代码易读性和组织性
添加精确查找功能，支持文件名严格匹配
"""

import sys
import os
from PyQt6.QtWidgets import QApplication

# 添加components路径到模块搜索路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 读取版本号
def get_version():
    """从 VERSION 文件读取版本号"""
    try:
        version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
        with open(version_file, 'r') as f:
            return f.read().strip()
    except:
        return "2.5.0"

__version__ = get_version()

from components.main_window import FileGatherPro


def main():
    """应用程序主函数"""
    app = QApplication(sys.argv)
    window = FileGatherPro()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
