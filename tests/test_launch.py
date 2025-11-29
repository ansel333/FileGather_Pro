#!/usr/bin/env python3
"""
FileGather Pro 启动测试脚本
检查所有依赖和环境，然后尝试启动应用
"""

import sys
import os

# 添加父目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_environment():
    """检查环境和依赖"""
    print("=" * 60)
    print("FileGather Pro v2.3.5 - 环境检查")
    print("=" * 60)
    
    # 检查 Python 版本
    print(f"\n[CHECK] Python 版本")
    print(f"  版本: {sys.version}")
    print(f"  可执行文件: {sys.executable}")
    
    # 检查关键模块
    print(f"\n[CHECK] 关键模块")
    modules = {
        'PyQt5': ('PyQt5', 'QtWidgets'),
        'reportlab': ('reportlab', 'lib'),
        'PyMuPDF': ('fitz',),
        'python-docx': ('docx',),
        'openpyxl': ('openpyxl',),
    }
    
    missing = []
    for pkg_name, import_names in modules.items():
        try:
            for import_name in import_names:
                __import__(import_name)
            print(f"  [OK] {pkg_name}")
        except ImportError as e:
            print(f"  [FAIL] {pkg_name}: {e}")
            missing.append(pkg_name)
    
    # 检查应用模块
    print(f"\n[CHECK] 应用模块")
    app_modules = [
        'components',
        'components.main_window',
        'components.ui_builder',
        'components.search_logic',
        'components.file_operations',
        'components.utils',
        'components.dialogs',
    ]
    
    for module in app_modules:
        try:
            __import__(module)
            print(f"  [OK] {module}")
        except ImportError as e:
            print(f"  [FAIL] {module}: {e}")
            missing.append(module)
    
    if missing:
        print(f"\n[WARNING] 缺失模块: {', '.join(missing)}")
        return False
    
    print(f"\n[SUCCESS] 所有检查通过!")
    return True

def try_launch_app():
    """尝试启动应用"""
    print("\n" + "=" * 60)
    print("启动应用")
    print("=" * 60)
    
    try:
        # 设置 GUI 环境
        os.environ['QT_API'] = 'pyqt5'
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'  # 如果没有 display
        
        print("\n[INFO] 导入应用模块...")
        from components import FileGatherPro
        from PyQt5.QtWidgets import QApplication
        
        print("[OK] 模块导入成功")
        
        print("\n[INFO] 创建应用实例...")
        app = QApplication([])
        print("[OK] QApplication 创建成功")
        
        print("\n[INFO] 创建主窗口...")
        window = FileGatherPro()
        print("[OK] 主窗口创建成功")
        
        print("\n[INFO] 显示窗口...")
        window.show()
        print("[OK] 窗口已显示")
        
        print("\n[INFO] 进入事件循环...")
        print("应用已启动! 按 Ctrl+C 退出")
        sys.exit(app.exec_())

    except Exception as e:
        print(f"\n[FAIL] 启动失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if check_environment():
        try_launch_app()
