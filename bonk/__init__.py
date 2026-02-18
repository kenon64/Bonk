"""
Bonk - Audio to MIDI Converter

Преобразование аудиофайлов в различных форматах в нотную запись (MIDI, MusicXML, PDF).
"""

__version__ = "1.0.0"
__author__ = "Bonk Team"

from .converter import AudioToMidiConverter
from .score_generator import ScoreGenerator

__all__ = ["AudioToMidiConverter", "ScoreGenerator"]
