# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file для Bonk - Audio to MIDI Converter

Используется для создания однофайлового exe-приложения
"""

import sys
from pathlib import Path

block_cipher = None

a = Analysis(
    ['bonk/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'librosa',
        'librosa.core',
        'librosa.util',
        'librosa.effects',
        'librosa.feature',
        'librosa.fft_frequencies',
        'librosa.frames_to_time',
        'librosa.note_to_hz',
        'librosa.midi_to_note',
        'librosa.stft',
        'librosa.pyin',
        'numpy',
        'scipy',
        'scipy.signal',
        'scipy.fft',
        'pretty_midi',
        'soundfile',
        'click',
        'audioread',
        'audioread.base',
        'audioread.soundfile',
        'music21',
        'music21.stream',
        'music21.note',
        'music21.tempo',
        'music21.meter',
        'music21.instrument',
        'music21.metadata',
        'matplotlib',
        'matplotlib.pyplot',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[
        'matplotlib',
        'pandas',
        'sklearn',
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
    name='bonk',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Консольное приложение
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Опционально: создать дополнительные артефакты для разработки
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='bonk',
# )
