"""
Модуль для генерации MIDI файлов.

Создаёт MIDI файл из обнаруженных нот.
"""

import pretty_midi
import numpy as np
from pathlib import Path
from typing import List


class MidiGenerator:
    """Генератор MIDI файлов."""

    def __init__(self, program: int = 0, velocity: int = 100):
        """
        Инициализация генератора MIDI.

        Args:
            program: MIDI программа инструмента (0-127). По умолчанию 0 = Acoustic Piano.
            velocity: Громкость ноты (0-127).
        """
        self.program = program
        self.velocity = velocity

    def create_midi_from_notes(
        self,
        midi_notes: np.ndarray,
        start_times: np.ndarray,
        durations: np.ndarray,
        tempo: int = 120,
    ) -> pretty_midi.PrettyMIDI:
        """
        Создать MIDI объект из нот.

        Args:
            midi_notes: Массив MIDI номеров нот.
            start_times: Массив времён начала нот в секундах.
            durations: Массив длительностей нот в секундах.
            tempo: Темп в BPM.

        Returns:
            MIDI объект (pretty_midi.PrettyMIDI).
        """
        midi_data = pretty_midi.PrettyMIDI(initial_tempo=tempo)

        # Создать инструмент (рояль)
        instrument = pretty_midi.Instrument(program=self.program)

        # Создать ноты
        for midi_note, start_time, duration in zip(midi_notes, start_times, durations):
            note = pretty_midi.Note(
                velocity=self.velocity,
                pitch=int(midi_note),
                start=float(start_time),
                end=float(start_time + duration),
            )
            instrument.notes.append(note)

        midi_data.instruments.append(instrument)

        return midi_data

    def save_midi(self, midi_data: pretty_midi.PrettyMIDI, output_path: str) -> None:
        """
        Сохранить MIDI объект в файл.

        Args:
            midi_data: MIDI объект.
            output_path: Путь для сохранения MIDI файла.

        Raises:
            IOError: Ошибка при записи файла.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            midi_data.write(str(output_path))
            print(f"✓ MIDI файл сохранён: {output_path}")
        except Exception as e:
            raise IOError(f"Ошибка при сохранении MIDI файла: {e}")

    def get_midi_info(self, midi_data: pretty_midi.PrettyMIDI) -> dict:
        """
        Получить информацию о MIDI файле.

        Args:
            midi_data: MIDI объект.

        Returns:
            Словарь с информацией о файле.
        """
        info = {
            "duration": midi_data.get_end_time(),
            "instruments": len(midi_data.instruments),
            "total_notes": sum(len(inst.notes) for inst in midi_data.instruments),
            "tempo": midi_data.get_tempo_changes()[0][0] if midi_data.get_tempo_changes() else 120,
        }

        return info
