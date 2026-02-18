"""
Пример использования Bonk как Python модуля.
"""

from bonk import AudioToMidiConverter

# Создание конвертера
converter = AudioToMidiConverter(sr=22050)

# Пример 1: Базовое преобразование в MIDI
print("=== Пример 1: Преобразование в MIDI ===")
try:
    converter.convert(
        input_path="examples/audio/example.wav",
        output_path="examples/output/example.mid",
        format="midi",
        verbose=True,
    )
except FileNotFoundError:
    print("⚠️  Файл с примером не найден. Создайте examples/audio/example.wav")


# Пример 2: Преобразование в MusicXML (нотная партитура)
print("\n=== Пример 2: Преобразование в MusicXML (НОТЫ!) ===")
try:
    converter.convert(
        input_path="examples/audio/music.mp3",
        output_path="examples/output/music.musicxml",
        min_duration=0.15,
        tempo=140,
        format="musicxml",  # ← НОТЫ на нотном стане!
        verbose=True,
    )
    print("💡 Совет: Откройте файл в MuseScore, Finale или Sibelius")
except FileNotFoundError:
    print("⚠️  Файл с примером не найден")


# Пример 3: Преобразование в PDF (готово к печати)
print("\n=== Пример 3: Преобразование в PDF (готово к печати) ===")
try:
    converter.convert(
        input_path="examples/audio/song.wav",
        output_path="examples/output/song.pdf",
        tempo=120,
        format="pdf",  # ← PDF с нотами!
        verbose=True,
    )
    print("💡 PDF можно распечатать и читать с листа!")
except FileNotFoundError:
    print("⚠️  Файл с примером не найден")
except Exception as e:
    print(f"⚠️  PDF требует MuseScore: {e}")


# Пример 3: Перехват ошибок
print("\n=== Пример 3: Обработка ошибок ===")
try:
    converter = AudioToMidiConverter(sr=16000)
    converter.convert(
        input_path="nonexistent.wav",
        output_path="output.mid",
    )
except FileNotFoundError as e:
    print(f"Ошибка: {e}")
except ValueError as e:
    print(f"Ошибка обработки: {e}")
except Exception as e:
    print(f"Неожиданная ошибка: {e}")


# Пример 4: Использование отдельных компонентов
print("\n=== Пример 4: Использование компонентов отдельно ===")
from bonk.audio_processor import AudioProcessor
from bonk.pitch_detector import PitchDetector
from bonk.midi_generator import MidiGenerator
from bonk.score_generator import ScoreGenerator

try:
    # Загрузить аудио
    processor = AudioProcessor(sr=22050)
    y, sr = processor.load_audio("examples/audio/sample.wav")
    print(f"✓ Аудио загружено: {len(y)} отсчётов")

    # Предварительная обработка
    y = processor.preprocess_audio(y, sr)
    print(f"✓ Аудио обработано")

    # Обнаружить высоту тона
    detector = PitchDetector(sr=sr)
    f0, times = detector.detect_pitch(y)
    print(f"✓ Высота тона обнаружена: {len(f0)} отсчётов")

    # Квантизировать ноты
    midi_notes, start_times, durations = detector.quantize_notes(f0, times)
    print(f"✓ Обнаружено нот: {len(midi_notes)}")

    # Создать и сохранить MIDI
    generator = MidiGenerator()
    midi_data = generator.create_midi_from_notes(
        midi_notes, start_times, durations, tempo=120
    )
    generator.save_midi(midi_data, "examples/output/sample.mid")

    # НОВОЕ: Создать и сохранить нотную партитуру (MusicXML)!
    score_gen = ScoreGenerator(tempo_bpm=120, title="Sample Score")
    score = score_gen.create_score_from_notes(
        midi_notes, start_times, durations
    )
    score_gen.save_musicxml(score, "examples/output/sample.musicxml")
    print(f"✓ MusicXML партитура сохранена (НОТЫ на нотном стане!)")

    # Получить информацию о партитуре
    info = score_gen.get_score_info(score)
    print(f"\nИнформация о партитуре:")
    print(f"  Название: {info['title']}")
    print(f"  Всего нот: {info['total_notes']}")
    print(f"  Длительность: {info['duration_seconds']:.2f} сек")

except FileNotFoundError:
    print("⚠️  Файл с примером не найден")
except Exception as e:
    print(f"Ошибка: {e}")
