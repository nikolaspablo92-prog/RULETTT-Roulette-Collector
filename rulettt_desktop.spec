# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller configuration для RULETTT Desktop
Создает standalone .exe файл для Windows
"""

block_cipher = None

a = Analysis(
    ['rulettt_desktop.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('webapp', 'webapp'),
        ('src', 'src'),
        ('data', 'data'),
        ('*.md', '.'),
        ('*.js', '.'),
        ('api_server.py', '.'),
    ],
    hiddenimports=[
        'flask',
        'flask_cors',
        'requests',
        'sqlite3',
        'json',
        'datetime',
        'pathlib',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PyQt5.QtWebEngineWidgets',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='RULETTT',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Без консоли
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='RULETTT',
)
