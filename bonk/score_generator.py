"""
Модуль для конвертации MIDI в нотную запись (MusicXML, PDF).

Преобразует MIDI данные в музыкальные объекты и экспортирует в:
- MusicXML (откроется в MuseScore, Finale, Sibelius)
- PDF партитура (готова к распечатке)
"""

import numpy as np
from pathlib import Path
from typing import Tuple, Optional

try:
    from music21 import stream, note, tempo, meter, instrument, metadata
    MUSIC21_AVAILABLE = True
except ImportError:
    MUSIC21_AVAILABLE = False


class ScoreGenerator:
    """Генератор нотной партитуры из MIDI данных."""

    def __init__(self, tempo_bpm: int = 120, title: str = "Score"):
        """
        Инициализация генератора партитуры.

        Args:
            tempo_bpm: Темп в BPM.
            title: Название композиции.
        """
        if not MUSIC21_AVAILABLE:
            raise ImportError(
                "Требуется music21 для работы с нотной партитурой. "
                "Установите: pip install music21"
            )

        self.tempo_bpm = tempo_bpm
        self.title = title

    def create_score_from_notes(
        self,
        midi_notes: np.ndarray,
        start_times: np.ndarray,
        durations: np.ndarray,
    ) -> stream.Score:
        """
        Создать музыкальную партитуру из нот.

        Args:
            midi_notes: Массив MIDI номеров нот.
            start_times: Массив времён начала в секундах.
            durations: Массив длительностей в секундах.

        Returns:
            music21 Score объект с партитурой.
        """
        # Создать партитуру
        s = stream.Score()
        part = stream.Part()

        # Установить инструмент (рояль)
        part.append(instrument.Piano())

        # Установить темп
        part.append(tempo.MetronomeMark(number=self.tempo_bpm))

        # Установить размер (4/4)
        part.append(meter.TimeSignature("4/4"))

        # Добавить метаданные
        s.metadata = metadata.Metadata()
        s.metadata.title = self.title
        s.metadata.composer = "Bonk - Auto-transcription"

        # Сортировать ноты по времени (на случай если не отсортированы)
        sorted_indices = np.argsort(start_times)
        midi_notes_sorted = midi_notes[sorted_indices]
        start_times_sorted = start_times[sorted_indices]
        durations_sorted = durations[sorted_indices]

        # Преобразовать абсолютное время в относительное
        current_time = 0.0
        for midi_note, start_time, duration in zip(
            midi_notes_sorted, start_times_sorted, durations_sorted
        ):
            # Добавить паузу если нужно
            if start_time > current_time:
                rest_duration = start_time - current_time
                rest = self._convert_duration_to_quarter_notes(rest_duration)
                if rest > 0:
                    part.append(note.Rest(quarterLength=rest))
                current_time = start_time

            # Добавить ноту
            n = note.Note(midi=int(midi_note))
            n.quarterLength = self._convert_duration_to_quarter_notes(duration)
            part.append(n)
            current_time = start_time + duration

        s.append(part)
        return s

    def _convert_duration_to_quarter_notes(self, duration_seconds: float) -> float:
        """
        Конвертировать длительность из секунд в четвертные доли.

        Args:
            duration_seconds: Длительность в секундах.

        Returns:
            Длительность в четвертных долях (quarter notes).
        """
        # Формула: quarter_notes = (seconds * tempo_bpm) / 60
        # где quarter_notes это доли четверти в темпе BPM
        quarter_notes = (duration_seconds * self.tempo_bpm) / 60
        return quarter_notes

    def save_musicxml(self, score: stream.Score, output_path: str) -> None:
        """
        Сохранить партитуру в MusicXML формат.

        Args:
            score: music21 Score объект.
            output_path: Путь для сохранения файла.

        Raises:
            IOError: Ошибка при записи файла.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Сохранить как MusicXML
            score.write("musicxml", fp=str(output_path))
            print(f"✓ MusicXML файл сохранён: {output_path}")
        except Exception as e:
            raise IOError(f"Ошибка при сохранении MusicXML: {e}")

    def save_pdf(self, score: stream.Score, output_path: str) -> None:
        """
        Сохранить партитуру в PDF формат.

        Требует MuseScore или другую программу нотной записи.

        Args:
            score: music21 Score объект.
            output_path: Путь для сохранения файла.

        Raises:
            IOError: Ошибка при записи файла или отсутствии MuseScore.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Попробовать сохранить как PDF через MuseScore
            score.write("pdf", fp=str(output_path))
            print(f"✓ PDF файл сохранён: {output_path}")
        except Exception as e:
            print(f"⚠️  Ошибка при сохранении PDF напрямую: {e}")
            print(
                "💡 Совет: Сохраните MusicXML и откройте в MuseScore для экспорта в PDF"
            )
            raise IOError(
                f"Ошибка при создании PDF. "
                f"Убедитесь что MuseScore или Finale установлены: {e}"
            )

    def show_score(self, score: stream.Score) -> None:
        """
        Показать партитуру (откроет в MuseScore или системной программе).

        Args:
            score: music21 Score объект.
        """
        try:
            score.show()
        except Exception as e:
            print(f"⚠️  Не удалось показать партитуру: {e}")
            print("💡 Совет: Сохраните в MusicXML и откройте в MuseScore вручную")

    def get_score_info(self, score: stream.Score) -> dict:
        """
        Получить информацию о партитуре.

        Args:
            score: music21 Score объект.

        Returns:
            Словарь с информацией о партитуре.
        """
        instruments = [p.getInstrument() for p in score.parts]
        total_notes = sum(
            len(p.flatten().getElementsByClass(note.Note)) for p in score.parts
        )
        total_rests = sum(
            len(p.flatten().getElementsByClass(note.Rest)) for p in score.parts
        )
        duration_ql = sum(p.duration.quarterLength for p in score.parts)

        info = {
            "title": (
                score.metadata.title if score.metadata and score.metadata.title else "Unknown"
            ),
            "instruments": len(score.parts),
            "total_notes": total_notes,
            "total_rests": total_rests,
            "duration_quarter_notes": duration_ql,
            "duration_seconds": (duration_ql * 60) / self.tempo_bpm,
        }

        return info
