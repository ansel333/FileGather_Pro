#!/usr/bin/env python3
"""
FileGather Pro Launch Test Script
Check all dependencies and environment, then attempt to launch the application
"""

import sys
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_environment():
    """Check environment and dependencies"""
    print("=" * 60)
    print("FileGather Pro v2.4.0 - Environment Check")
    print("=" * 60)
    
    # Check Python version
    print(f"\n[CHECK] Python Version")
    print(f"  Version: {sys.version}")
    print(f"  Executable: {sys.executable}")
    
    # Check key modules
    print(f"\n[CHECK] Key Modules")
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
    
    # Check application modules
    print(f"\n[CHECK] Application Modules")
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
        print(f"\n[WARNING] Missing modules: {', '.join(missing)}")
        return False
    
    print(f"\n[SUCCESS] All checks passed!")
    return True

def try_launch_app():
    """Try to launch the application"""
    print("\n" + "=" * 60)
    print("Launch Application")
    print("=" * 60)
    
    try:
        # Configure GUI environment
        os.environ['QT_API'] = 'pyqt5'
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'  # If no display available
        
        print("\n[INFO] Importing application modules...")
        from components import FileGatherPro
        from PyQt5.QtWidgets import QApplication
        
        print("[OK] Module import successful")
        
        print("\n[INFO] Creating application instance...")
        app = QApplication([])
        print("[OK] QApplication created successfully")
        
        print("\n[INFO] Creating main window...")
        window = FileGatherPro()
        print("[OK] Main window created successfully")
        
        print("\n[INFO] Displaying window...")
        window.show()
        print("[OK] Window displayed")
        
        print("\n[INFO] Entering event loop...")
        print("Application started! Press Ctrl+C to exit")
        sys.exit(app.exec_())

    except Exception as e:
        print(f"\n[FAIL] Launch failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if check_environment():
        try_launch_app()
