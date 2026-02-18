"""
Модуль для обнаружения высоты тона (pitch detection).

Использует различные методы для определения основной частоты звуков.
"""

import numpy as np
import librosa
from typing import Tuple, Optional


class PitchDetector:
    """Детектор высоты тона."""

    # MIDI номер для A4 = 69, частота = 440 Гц
    A4_MIDI = 69
    A4_FREQ = 440.0

    def __init__(self, sr: int = 22050, hop_length: int = 512):
        """
        Инициализация детектора высоты тона.

        Args:
            sr: Частота дискретизации.
            hop_length: Количество отсчётов между кадрами.
        """
        self.sr = sr
        self.hop_length = hop_length

    def detect_pitch(self, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Обнаружить высоту тона методом пиподсчёта (pyin).

        Args:
            y: Аудиоданные.

        Returns:
            Кортеж (f0 частоты, время отсчётов).
        """
        f0, voiced_flag, voiced_probs = librosa.pyin(
            y,
            fmin=librosa.note_to_hz("C2"),
            fmax=librosa.note_to_hz("C8"),
            sr=self.sr,
            hop_length=self.hop_length,
        )

        times = librosa.frames_to_time(np.arange(len(f0)), sr=self.sr, hop_length=self.hop_length)

        return f0, times

    def freq_to_midi(self, freq: float) -> Optional[int]:
        """
        Преобразовать частоту в MIDI ноту.

        Args:
            freq: Частота в Гц.

        Returns:
            MIDI номер (0-127) или None если частота недействительна.
        """
        if freq <= 0 or np.isnan(freq):
            return None

        # Формула: MIDI = 69 + 12 * log2(frequency / 440)
        midi_note = self.A4_MIDI + 12 * np.log2(freq / self.A4_FREQ)

        # Округлить до ближайшей ноты
        midi_note = round(midi_note)

        # Проверить диапазон MIDI (0-127)
        if 0 <= midi_note <= 127:
            return int(midi_note)
        return None

    def quantize_notes(
        self, f0: np.ndarray, times: np.ndarray, min_duration: float = 0.1
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Квантизировать обнаруженные ноты.

        Группирует близкие ноты в одну и удаляет очень короткие ноты.

        Args:
            f0: Обнаруженные частоты.
            times: Времена отсчётов.
            min_duration: Минимальная длительность ноты в секундах.

        Returns:
            Кортеж (MIDI ноты, времена начала, длительности).
        """
        # Преобразовать частоты в MIDI номера
        midi_notes = []
        valid_times = []

        for freq, t in zip(f0, times):
            midi = self.freq_to_midi(freq)
            if midi is not None:
                midi_notes.append(midi)
                valid_times.append(t)

        if not midi_notes:
            return np.array([], dtype=int), np.array([]), np.array([])

        midi_notes = np.array(midi_notes)
        valid_times = np.array(valid_times)

        # Группировка близких нот
        notes_list = []
        start_idx = 0

        for i in range(1, len(midi_notes) + 1):
            # Если нота изменилась или это последний отсчёт
            if i == len(midi_notes) or midi_notes[i] != midi_notes[i - 1]:
                duration = valid_times[i - 1] - valid_times[start_idx]

                # Пропустить ноты меньше min_duration
                if duration >= min_duration:
                    notes_list.append(
                        {
                            "midi": int(midi_notes[start_idx]),
                            "start_time": float(valid_times[start_idx]),
                            "duration": float(duration),
                        }
                    )

                start_idx = i

        result_midi = np.array([n["midi"] for n in notes_list], dtype=int)
        result_start = np.array([n["start_time"] for n in notes_list], dtype=float)
        result_duration = np.array([n["duration"] for n in notes_list], dtype=float)

        return result_midi, result_start, result_duration

    def midi_to_note_name(self, midi_note: int) -> str:
        """
        Преобразовать MIDI номер в название ноты.

        Args:
            midi_note: MIDI номер (0-127).

        Returns:
            Название ноты (например, "C4", "A#5").
        """
        return librosa.midi_to_note(midi_note)
