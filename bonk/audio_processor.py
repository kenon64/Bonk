"""
Модуль для обработки аудиофайлов.

Загружает аудиофайлы различных форматов и подготавливает их к анализу.
"""

import librosa
import numpy as np
from pathlib import Path
from typing import Tuple


class AudioProcessor:
    """Обработчик аудиофайлов."""

    def __init__(self, sr: int = 22050):
        """
        Инициализация процессора аудио.

        Args:
            sr: Частота дискретизации (sample rate) в Гц.
        """
        self.sr = sr

    def load_audio(self, file_path: str) -> Tuple[np.ndarray, int]:
        """
        Загрузить аудиофайл.

        Поддерживаемые форматы: WAV, MP3, OGG, FLAC и др.

        Args:
            file_path: Путь к аудиофайлу.

        Returns:
            Кортеж (аудиоданные, частота дискретизации).

        Raises:
            FileNotFoundError: Файл не найден.
            ValueError: Неподдерживаемый формат файла.
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        try:
            y, sr = librosa.load(str(file_path), sr=self.sr, mono=True)
            return y, sr
        except Exception as e:
            raise ValueError(f"Ошибка при загрузке файла: {e}")

    def preprocess_audio(self, y: np.ndarray, sr: int) -> np.ndarray:
        """
        Предварительная обработка аудио.

        Применяет фильтрацию и нормализацию.

        Args:
            y: Аудиоданные.
            sr: Частота дискретизации.

        Returns:
            Обработанные аудиоданные.
        """
        # Нормализация
        y = librosa.util.normalize(y)

        # Удаление низких частот (шума)
        y = librosa.effects.trim(y, top_db=40)[0]

        return y

    def get_magnitude_spectrum(
        self, y: np.ndarray, sr: int, n_fft: int = 2048
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Получить спектр мощности аудио.

        Args:
            y: Аудиоданные.
            sr: Частота дискретизации.
            n_fft: Размер преобразования Фурье.

        Returns:
            Кортеж (частоты, магнитуда).
        """
        D = librosa.stft(y, n_fft=n_fft)
        magnitude = np.abs(D)
        frequencies = librosa.fft_frequencies(sr=sr, n_fft=n_fft)

        return frequencies, magnitude

    def get_energy_envelope(self, y: np.ndarray, sr: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Получить огибающую энергии сигнала.

        Args:
            y: Аудиоданные.
            sr: Частота дискретизации.

        Returns:
            Кортеж (времена, энергия).
        """
        S = librosa.feature.melspectrogram(y=y, sr=sr)
        energy = librosa.feature.rms(S=S)[0]
        times = librosa.frames_to_time(np.arange(len(energy)), sr=sr)

        return times, energy
