# -*- mode: python ; coding: utf-8 -*-

import os
import qt_themes
from PyInstaller.utils.hooks import collect_data_files

# collect all theme files from qt_themes package
datas = collect_data_files("qt_themes", subdir="themes")
datas.append(('.env', '.'))
datas.append(('assets/images/*.*', 'assets/images'))
a = Analysis(
    ['main.py'],
    pathex=[os.path.abspath(".")],
    binaries=[],
    datas=datas,
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='PySideAlchemy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PySideAlchemy',
)
