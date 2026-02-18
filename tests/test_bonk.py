"""
Тесты для модуля Bonk.
"""

import numpy as np
import pytest
from bonk.pitch_detector import PitchDetector
from bonk.audio_processor import AudioProcessor
from bonk.midi_generator import MidiGenerator


class TestPitchDetector:
    """Тесты для обнаружения высоты тона."""

    def setup_method(self):
        """Подготовка к тестам."""
        self.detector = PitchDetector(sr=22050, hop_length=512)

    def test_freq_to_midi_concert_a(self):
        """Тест преобразования A4 (440 Гц) в MIDI."""
        # A4 = 440 Гц = MIDI номер 69
        midi = self.detector.freq_to_midi(440.0)
        assert midi == 69

    def test_freq_to_midi_invalid(self):
        """Тест преобразования недействительной частоты."""
        # NaN частота
        midi = self.detector.freq_to_midi(np.nan)
        assert midi is None

        # Нулевая частота
        midi = self.detector.freq_to_midi(0)
        assert midi is None

        # Отрицательная частота
        midi = self.detector.freq_to_midi(-100)
        assert midi is None

    def test_midi_to_note_name(self):
        """Тест преобразования MIDI номера в название ноты."""
        # MIDI 69 = A4
        note = self.detector.midi_to_note_name(69)
        assert note == "A4"

        # MIDI 60 = C4
        note = self.detector.midi_to_note_name(60)
        assert note == "C4"

    def test_quantize_notes_empty(self):
        """Тест квантизации пустого массива нот."""
        f0 = np.array([])
        times = np.array([])

        midi_notes, start_times, durations = self.detector.quantize_notes(f0, times)

        assert len(midi_notes) == 0
        assert len(start_times) == 0
        assert len(durations) == 0

    def test_quantize_notes_single(self):
        """Тест квантизации одной ноты."""
        f0 = np.array([440.0, 440.0, 440.0])
        times = np.array([0.0, 0.05, 0.1])

        midi_notes, start_times, durations = self.detector.quantize_notes(
            f0, times, min_duration=0.08
        )

        assert len(midi_notes) == 1
        assert midi_notes[0] == 69
        assert start_times[0] == 0.0
        assert durations[0] == pytest.approx(0.1, abs=0.01)


class TestAudioProcessor:
    """Тесты для обработки аудио."""

    def setup_method(self):
        """Подготовка к тестам."""
        self.processor = AudioProcessor(sr=22050)

    def test_load_audio_nonexistent(self):
        """Тест загрузки несуществующего файла."""
        with pytest.raises(FileNotFoundError):
            self.processor.load_audio("nonexistent_file.wav")

    def test_preprocess_audio(self):
        """Тест предварительной обработки."""
        y = np.random.randn(22050)  # 1 секунда на 22050 Гц
        y_processed = self.processor.preprocess_audio(y, self.processor.sr)

        assert len(y_processed) > 0
        assert np.max(np.abs(y_processed)) <= 1.0  # Нормализовано


class TestMidiGenerator:
    """Тесты для генерации MIDI."""

    def setup_method(self):
        """Подготовка к тестам."""
        self.generator = MidiGenerator(program=0, velocity=100)

    def test_create_midi_from_notes(self):
        """Тест создания MIDI из нот."""
        midi_notes = np.array([60, 62, 64, 65])  # C4, D4, E4, F4
        start_times = np.array([0.0, 1.0, 2.0, 3.0])
        durations = np.array([1.0, 1.0, 1.0, 1.0])

        midi_data = self.generator.create_midi_from_notes(
            midi_notes, start_times, durations, tempo=120
        )

        assert len(midi_data.instruments) == 1
        assert len(midi_data.instruments[0].notes) == 4

    def test_get_midi_info(self):
        """Тест получения информации о MIDI."""
        midi_notes = np.array([69])
        start_times = np.array([0.0])
        durations = np.array([1.0])

        midi_data = self.generator.create_midi_from_notes(
            midi_notes, start_times, durations, tempo=120
        )

        info = self.generator.get_midi_info(midi_data)

        assert info["total_notes"] == 1
        assert info["tempo"] == 120
        assert info["instruments"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
