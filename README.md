# Bonk - Audio to MIDI Converter

Программа для преобразования аудиофайлов в различных форматах в нотную запись (MIDI).

## Возможности

- ✅ Поддержка аудиоформатов: MP3, WAV, OGG, FLAC и др.
- ✅ Обнаружение высоты тона (pitch detection)
- ✅ Автоматическая квантизация нот
- ✅ Преобразование в MIDI формат
- ✅ Команднострочный интерфейс (CLI)

## Установка

```bash
pip install -r requirements.txt
```

## Использование

### CLI
```bash
python -m bonk convert input.mp3 output.mid
```

### Python код
```python
from bonk.converter import AudioToMidiConverter

converter = AudioToMidiConverter()
converter.convert('audio.wav', 'output.mid')
```

## Зависимости

- **librosa** - анализ и обработка аудио
- **numpy** - числовые вычисления
- **pretty_midi** - создание MIDI файлов
- **scipy** - обработка сигналов
- **click** - интерфейс командной строки

## Структура проекта

```
bonk/
├── __init__.py
├── converter.py          # Основной конвертер
├── audio_processor.py    # Обработка аудио
├── pitch_detector.py     # Обнаружение высоты тона
├── midi_generator.py     # Генерация MIDI
└── cli.py               # Интерфейс командной строки
```

## Примеры

### Простое преобразование
```bash
python -m bonk convert song.mp3 output.mid
```

### С параметрами
```bash
python -m bonk convert song.wav output.mid --sr 22050 --threshold 0.1
```

## Лицензия

MIT