"""
Основной модуль конвертера аудио в MIDI и нотную запись.

Объединяет все компоненты для преобразования аудиофайлов в:
- MIDI
- MusicXML (открывается в MuseScore, Finale, Sibelius)
- PDF партитура
"""

from pathlib import Path
from typing import Optional

from .audio_processor import AudioProcessor
from .pitch_detector import PitchDetector
from .midi_generator import MidiGenerator
from .score_generator import ScoreGenerator


class AudioToMidiConverter:
    """Конвертер аудиофайлов в MIDI."""

    def __init__(self, sr: int = 22050, hop_length: int = 512):
        """
        Инициализация конвертера.

        Args:
            sr: Частота дискретизации в Гц.
            hop_length: Количество отсчётов между кадрами.
        """
        self.sr = sr
        self.hop_length = hop_length
        self.audio_processor = AudioProcessor(sr=sr)
        self.pitch_detector = PitchDetector(sr=sr, hop_length=hop_length)
        self.midi_generator = MidiGenerator()

    def convert(
        self,
        input_path: str,
        output_path: str,
        min_duration: float = 0.1,
        tempo: int = 120,
        format: str = "midi",
        verbose: bool = True,
    ) -> None:
        """
        Преобразовать аудиофайл в MIDI, MusicXML или PDF.

        Args:
            input_path: Путь к входному аудиофайлу.
            output_path: Путь для сохранения файла.
            min_duration: Минимальная длительность ноты в секундах.
            tempo: Темп в BPM.
            format: Формат выхода ('midi', 'musicxml', 'pdf').
            verbose: Выводить ли информацию о процессе.

        Raises:
            FileNotFoundError: Входной файл не найден.
            ValueError: Ошибка при обработке файла.
        """
        input_path = Path(input_path)
        output_path = Path(output_path)

        if verbose:
            print(f"📂 Загрузка: {input_path}")

        # Загрузить аудио
        y, sr = self.audio_processor.load_audio(str(input_path))

        if verbose:
            print(f"🔊 Длительность: {len(y) / sr:.2f} сек, SR: {sr} Гц")

        # Предварительная обработка
        if verbose:
            print("🔧 Предварительная обработка...")
        y = self.audio_processor.preprocess_audio(y, sr)

        # Обнаружить высоту тона
        if verbose:
            print("🎵 Обнаружение высоты тона...")
        f0, times = self.pitch_detector.detect_pitch(y)

        # Квантизировать ноты
        if verbose:
            print("📐 Квантизация нот...")
        midi_notes, start_times, durations = self.pitch_detector.quantize_notes(
            f0, times, min_duration=min_duration
        )

        if len(midi_notes) == 0:
            raise ValueError("Не обнаружено нот в аудиофайле")

        if verbose:
            print(f"📝 Обнаружено нот: {len(midi_notes)}")

        # Создать MIDI
        if verbose:
            print("🎹 Создание MIDI...")
        midi_data = self.midi_generator.create_midi_from_notes(
            midi_notes, start_times, durations, tempo=tempo
        )

        # Сохранить в зависимости от формата
        if format.lower() == "midi":
            self.midi_generator.save_midi(midi_data, str(output_path))
            if verbose:
                info = self.midi_generator.get_midi_info(midi_data)
                print(f"✅ Успешно!")
                print(f"   Длительность: {info['duration']:.2f} сек")
                print(f"   Всего нот: {info['total_notes']}")

        elif format.lower() in ["musicxml", "xml"]:
            if verbose:
                print("📄 Создание нотной партитуры...")
            score_gen = ScoreGenerator(tempo_bpm=tempo, title=input_path.stem)
            score = score_gen.create_score_from_notes(midi_notes, start_times, durations)
            score_gen.save_musicxml(score, str(output_path))
            if verbose:
                info = score_gen.get_score_info(score)
                print(f"✅ Успешно!")
                print(f"   Название: {info['title']}")
                print(f"   Всего нот: {info['total_notes']}")
                print(f"   Длительность: {info['duration_seconds']:.2f} сек")

        elif format.lower() == "pdf":
            if verbose:
                print("📄 Создание PDF партитуры...")
            score_gen = ScoreGenerator(tempo_bpm=tempo, title=input_path.stem)
            score = score_gen.create_score_from_notes(midi_notes, start_times, durations)
            score_gen.save_pdf(score, str(output_path))
            if verbose:
                info = score_gen.get_score_info(score)
                print(f"✅ Успешно!")
                print(f"   Название: {info['title']}")
                print(f"   Всего нот: {info['total_notes']}")
                print(f"   Длительность: {info['duration_seconds']:.2f} сек")

        else:
            raise ValueError(
                f"Неизвестный формат: {format}. "
                f"Доступные форматы: midi, musicxml, pdf"
            )
