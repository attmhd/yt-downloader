# -*- mode: python ; coding: utf-8 -*-
import os
import customtkinter

ctk_path = os.path.dirname(customtkinter.__file__)

block_cipher = None

binaries_to_add = []
if os.path.exists('ffmpeg.exe'):
    binaries_to_add.append(('ffmpeg.exe', '.'))
if os.path.exists('ffprobe.exe'):
    binaries_to_add.append(('ffprobe.exe', '.'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries_to_add,
    datas=[
        (ctk_path, 'customtkinter/'),
    ],
    hiddenimports=[
        'yt_dlp',
        'yt_dlp.extractor',
        'yt_dlp.downloader',
        'yt_dlp.postprocessor',
        'customtkinter',
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Modern-YT-Downloader',
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
)
