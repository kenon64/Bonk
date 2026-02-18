# Bonk - Audio to MIDI Converter

Полнофункциональная программа для преобразования аудиофайлов в различных форматах в нотную запись (MIDI).

## 🎵 Основные возможности

### ✅ Основной функционал
- **Поддержка форматов**: MP3, WAV, OGG, FLAC и другие форматы, поддерживаемые librosa
- **Обнаружение высоты тона**: Использует алгоритм PYIN (Probabilistic YIN) для точного определения высоты
- **Квантизация нот**: Автоматическое распознавание и группировка нот
- **Генерация MIDI**: Сохранение результатов в стандартный MIDI формат
- **Командная строка**: Удобный CLI интерфейс

### 🎛️ Настройки
- Частотная дискретизация (sample rate)
- Минимальная длительность ноты
- Темп (BPM)
- Выбор инструмента MIDI

## 📦 Установка

### Требования
- Python 3.8+
- FFmpeg (для поддержки MP3 и других форматов)

### Из исходного кода

```bash
# Клонирование репозитория
git clone https://github.com/kenon64/Bonk.git
cd Bonk

# Создание виртуального окружения (опционально)
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt

# Установка Bonk
pip install -e .
```

### После установки

```bash
# Зависит система может потребоваться установить FFmpeg
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Windows:
# Установить с https://ffmpeg.org/download.html
```

## 🚀 Использование

### Командная строка

#### Базовое использование

```bash
bonk convert input.wav output.mid
```

#### С параметрами

```bash
# Установить темп 140 BPM
bonk convert song.mp3 music.mid --tempo 140

# Установить минимальную длительность ноты 0.15 сек
bonk convert audio.wav out.mid --min-duration 0.15

# Установить частоту дискретизации
bonk convert audio.wav out.mid --sr 16000

# Подавить вывод информации
bonk convert input.wav output.mid --quiet
```

#### Получить информацию об аудиофайле

```bash
bonk info song.wav
```

### Python код

#### Простое использование

```python
from bonk import AudioToMidiConverter

# Создать конвертер
converter = AudioToMidiConverter()

# Преобразовать файл
converter.convert(
    input_path="song.mp3",
    output_path="song.mid"
)
```

#### Расширенное использование

```python
from bonk import AudioToMidiConverter

converter = AudioToMidiConverter(
    sr=22050,        # Частота дискретизации
    hop_length=512   # Размер окна для анализа
)

converter.convert(
    input_path="audio.wav",
    output_path="music.mid",
    min_duration=0.15,  # Минимальная длительность ноты (сек)
    tempo=120,          # Темп в BPM
    verbose=True        # Выводить информацию о процессе
)
```

#### Использование компонентов отдельно

```python
from bonk.audio_processor import AudioProcessor
from bonk.pitch_detector import PitchDetector
from bonk.midi_generator import MidiGenerator
import numpy as np

# Загрузить аудио
processor = AudioProcessor(sr=22050)
y, sr = processor.load_audio("audio.wav")

# Предварительная обработка
y = processor.preprocess_audio(y, sr)

# Обнаружить высоту тона
detector = PitchDetector(sr=sr)
f0, times = detector.detect_pitch(y)

# Квантизировать ноты
midi_notes, start_times, durations = detector.quantize_notes(f0, times)

# Создать и сохранить MIDI
generator = MidiGenerator()
midi_data = generator.create_midi_from_notes(
    midi_notes, start_times, durations, tempo=120
)
generator.save_midi(midi_data, "output.mid")
```

## 📋 API Документация

### AudioToMidiConverter

Главный класс для преобразования аудио в MIDI.

```python
converter = AudioToMidiConverter(sr=22050, hop_length=512)
converter.convert(input_path, output_path, min_duration=0.1, tempo=120, verbose=True)
```

**Параметры:**
- `sr` (int): Частота дискретизации в Гц. По умолчанию 22050
- `hop_length` (int): Количество отсчётов между кадрами. По умолчанию 512

**Методы:**
- `convert(input_path, output_path, min_duration=0.1, tempo=120, verbose=True)`: Преобразовать аудиофайл в MIDI

### AudioProcessor

Обработчик аудиофайлов.

```python
processor = AudioProcessor(sr=22050)
y, sr = processor.load_audio("audio.wav")
y = processor.preprocess_audio(y, sr)
```

**Методы:**
- `load_audio(file_path)`: Загрузить аудиофайл
- `preprocess_audio(y, sr)`: Предварительная обработка (нормализация, удаление шума)
- `get_magnitude_spectrum(y, sr, n_fft)`: Получить спектр мощности
- `get_energy_envelope(y, sr)`: Получить огибающую энергии

### PitchDetector

Обнаружение высоты тона.

```python
detector = PitchDetector(sr=22050, hop_length=512)
f0, times = detector.detect_pitch(y)
midi_notes, start_times, durations = detector.quantize_notes(f0, times)
```

**Методы:**
- `detect_pitch(y)`: Обнаружить высоту тона (возвращает частоты и времена)
- `quantize_notes(f0, times, min_duration)`: Квантизировать обнаруженные ноты
- `freq_to_midi(freq)`: Преобразовать частоту в MIDI номер
- `midi_to_note_name(midi_note)`: Преобразовать MIDI номер в название (например, C4)

### MidiGenerator

Генерация MIDI файлов.

```python
generator = MidiGenerator(program=0, velocity=100)
midi_data = generator.create_midi_from_notes(midi_notes, start_times, durations)
generator.save_midi(midi_data, "output.mid")
```

**Методы:**
- `create_midi_from_notes(midi_notes, start_times, durations, tempo)`: Создать MIDI объект
- `save_midi(midi_data, output_path)`: Сохранить MIDI в файл
- `get_midi_info(midi_data)`: Получить информацию о MIDI

## 🔧 Параметры CLI

### convert

```
bonk convert INPUT OUTPUT [OPTIONS]

OPTIONS:
  --sr INTEGER              Частота дискретизации (default: 22050)
  --hop-length INTEGER      Размер окна (default: 512)
  --min-duration FLOAT      Минимальная длительность ноты сек (default: 0.1)
  --tempo INTEGER           Темп в BPM (default: 120)
  --quiet                   Не выводить информацию
  --help                    Показать справку
```

### info

```
bonk info INPUT [OPTIONS]

OPTIONS:
  --sr INTEGER              Частота дискретизации (default: 22050)
  --help                    Показать справку
```

## 📊 Примеры

### Пример 1: Простое преобразование

```bash
bonk convert acoustic_guitar.wav guitar.mid
```

**Вывод:**
```
📂 Загрузка: acoustic_guitar.wav
🔊 Длительность: 5.23 сек, SR: 22050 Гц
🔧 Предварительная обработка...
🎵 Обнаружение высоты тона...
📐 Квантизация нот...
📝 Обнаружено нот: 47
🎹 Создание MIDI...
✓ MIDI файл сохранён: guitar.mid
✅ Успешно!
   Длительность: 5.18 сек
   Всего нот: 47
```

### Пример 2: Преобразование с параметрами

```bash
bonk convert vocal.mp3 vocal.mid --tempo 110 --min-duration 0.12
```

### Пример 3: Получить информацию о файле

```bash
bonk info song.wav
```

**Вывод:**
```
📂 Файл: song.wav
⏱️  Длительность: 3.45 сек
🔊 Частота дискретизации: 22050 Гц
📊 Количество отсчётов: 76050
```

## ⚙️ Структура проекта

```
Bonk/
├── README.md                 # Этот файл
├── CONTRIBUTING.md           # Руководство по участию
├── requirements.txt          # Зависимости
├── setup.py                  # Setup script
├── example_usage.py          # Примеры использования
│
├── bonk/                     # Основной пакет
│   ├── __init__.py          # Инициализация пакета
│   ├── __main__.py          # Точка входа для модуля
│   ├── cli.py               # Интерфейс командной строки
│   ├── converter.py         # Основной конвертер
│   ├── audio_processor.py   # Обработка аудио
│   ├── pitch_detector.py    # Обнаружение высоты
│   └── midi_generator.py    # Генерация MIDI
│
└── tests/                    # Тесты
    ├── __init__.py
    └── test_bonk.py         # Основные тесты
```

## 🧪 Тестирование

```bash
# Запустить все тесты
pytest tests/

# С подробным выводом
pytest tests/ -v

# С информацией о покрытии
pytest tests/ --cov=bonk
```

## 📝 Лицензия

MIT License - see LICENSE file for details

## 🤝 Участие

Приветствуются pull requests и issues! Подробнее в [CONTRIBUTING.md](CONTRIBUTING.md)

## ⚠️ Известные ограничения и будущие улучшения

### Текущие ограничения
- Лучше работает с монофоническим звуком (один голос)
- Полифонические записи (несколько голосов одновременно) распознаются менее точно
- Сложные гармонии могут быть упрощены
- Очень короткие ноты могут быть пропущены

### Планируемые улучшения
- [ ] Поддержка полифонического звука
- [ ] Экспорт в MusicXML
- [ ] GUI интерфейс
- [ ] Улучшенное обнаружение ритма
- [ ] Поддержка нескольких инструментов
- [ ] Обнаружение аккордов
- [ ] Предпросмотр результатов в реальном времени

## 💡 Советы по использованию

### Качество результатов
1. **Чистые записи**: Программа работает лучше с чистыми записями без фонового шума
2. **Монофонический звук**: Лучший результат с одним голосом или инструментом
3. **Продолжительность нот**: Установите `--min-duration` в соответствии с музыкой
4. **Темп**: Правильный темп улучшает читаемость MIDI

### Обработка MP3
Убедитесь, что FFmpeg установлен для работы с MP3:
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

### Оптимизация для разных инструментов
```bash
# Высокие голоса (более чувствительно)
bonk convert vocal_high.wav out.mid --min-duration 0.05

# Низкие голоса
bonk convert vocal_bass.wav out.mid --min-duration 0.2

# Инструменты со стакато
bonk convert staccato.wav out.mid --min-duration 0.08
```

## 📞 Поддержка

Если у вас есть вопросы или проблемы:
1. Проверьте [issues](https://github.com/kenon64/Bonk/issues)
2. Создайте новый issue с подробным описанием
3. Укажите команду, которую вы использовали, и понимаемый результат

## 🎯 Краткий старт

```bash
# Установка
pip install -r requirements.txt

# Преобразование
bonk convert sample.wav output.mid

# Готово! Откройте output.mid в музыкальном редакторе
```
