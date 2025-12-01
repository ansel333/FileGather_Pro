# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['FileGather_Pro.py'],
    pathex=[],
    binaries=[],
    datas=[('components', 'components')],
    hiddenimports=[
        'components.functions',
        'components.functions.folder_manager',
        'components.functions.search_manager',
        'components.functions.search_operations',
        'components.functions.results_manager',
        'components.functions.file_operations_ui',
        'components.functions.ui_interactions',
        'components.dialogs',
        'components.dialogs.search_result_dialog',
        'components.dialogs.conflict_dialog',
        'components.dialogs.pdf_generator',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='FileGather_Pro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['app.ico'],
)
