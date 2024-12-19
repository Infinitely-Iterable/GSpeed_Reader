# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.compat import is_linux

block_cipher = None

# Add system-wide Python packages
sys.path.append('/usr/lib/python3/dist-packages')

# Add Python shared library
binaries = [
    ('/usr/lib/x86_64-linux-gnu/libpython3.12.so.1.0', '.'),
    ('/usr/lib/x86_64-linux-gnu/libpython3.12.so.1', '.'),
    ('/usr/lib/x86_64-linux-gnu/libpython3.12.so', '.'),
]

# Collect all package data
datas = [
    ('/usr/lib/python3/dist-packages/markdown', 'markdown'),
    ('/usr/lib/python3/dist-packages/bs4', 'bs4'),
    ('/usr/lib/python3/dist-packages/jaraco', 'jaraco'),
    ('/usr/lib/python3/dist-packages/more_itertools', 'more_itertools'),
    ('/usr/lib/python3/dist-packages/platformdirs', 'platformdirs'),
    ('/usr/lib/python3/dist-packages/pkg_resources', 'pkg_resources'),
    ('/usr/lib/python3/dist-packages/setuptools', 'setuptools'),
    ('/usr/lib/python3/dist-packages/ttkthemes', 'ttkthemes'),
]

# All required imports
hiddenimports = [
    # Core dependencies
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'json',
    'os',
    'glob',
    
    # Main packages
    'markdown',
    'bs4',
    'beautifulsoup4',
    'ttkthemes',
    
    # Setup tools and resources
    'pkg_resources',
    'setuptools',
    'importlib_metadata',
    
    # Jaraco packages
    'jaraco',
    'jaraco.text',
    'jaraco.functools',
    'jaraco.context',
    
    # More itertools
    'more_itertools',
    'more_itertools.more',
    'more_itertools.recipes',
    
    # Platform dirs
    'platformdirs',
    'platformdirs.unix',
    'platformdirs.api',
    'platformdirs.version',
    
    # Additional tkinter modules
    'tkinter.constants',
    'tkinter.commondialog',
    '_tkinter',
]

a = Analysis(
    ['Obsidian_Reader.py'],
    pathex=[
        '/usr/lib/python3/dist-packages',
        '/usr/lib/python3.12/lib-dynload',
        '/usr/lib/python3/dist-packages/more_itertools',
        '/usr/lib/python3/dist-packages/platformdirs',
        '/usr/lib/python3/dist-packages/pkg_resources',
        '/usr/lib/python3/dist-packages/setuptools',
        '/usr/lib/python3/dist-packages/ttkthemes',
    ],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

# Ensure all package files are included
packages_to_include = ['more_itertools', 'platformdirs', 'pkg_resources', 'setuptools', 'ttkthemes']
for package in packages_to_include:
    package_path = f'/usr/lib/python3/dist-packages/{package}'
    if os.path.exists(package_path):
        a.datas += [(f'{package}/{x}', f'{package_path}/{x}', 'DATA')
                   for x in os.listdir(package_path)
                   if x.endswith('.py') or x.endswith('.json') or x.endswith('.tcl')]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Obsidian_Reader',
    debug=False,  # Disable debug mode
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Hide console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='../icon_assets/icon.png'
)
