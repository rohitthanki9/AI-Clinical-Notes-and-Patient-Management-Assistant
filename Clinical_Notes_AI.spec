# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Clinical Notes AI
Usage: pyinstaller Clinical_Notes_AI.spec
"""

import sys
from pathlib import Path

block_cipher = None

# Determine the separator based on platform
if sys.platform == 'win32':
    sep = ';'
else:
    sep = ':'

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('prompts', 'prompts'),
        ('assets', 'assets'),
    ],
    hiddenimports=[
        'whisper',
        'ttkbootstrap',
        'sounddevice',
        'soundfile',
        'tkinter',
        'sqlite3',
        'docx',
        'reportlab',
        'cryptography',
        'requests',
        'numpy',
        'PIL',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'pandas',
        'pytest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Clinical Notes AI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if Path('assets/icon.ico').exists() else None,
)

# For macOS
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='Clinical Notes AI.app',
        icon='assets/icon.icns' if Path('assets/icon.icns').exists() else None,
        bundle_identifier='com.clinicalnotes.ai',
    )
