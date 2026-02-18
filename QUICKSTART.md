Bonk - Audio to MIDI Converter
==============================

## Быстрый старт

### 1. Установка
```bash
pip install -r requirements.txt
```

### 2. Использование
```bash
# Основная команда
bonk convert input.wav output.mid

# С параметрами
bonk convert song.mp3 music.mid --tempo 140 --min-duration 0.1

# Получить информацию о файле
bonk info audio.wav
```

### 3. В Python коде
```python
from bonk import AudioToMidiConverter

converter = AudioToMidiConverter()
converter.convert('audio.wav', 'music.mid')
```

## 📚 Документация

- [DOCUMENTATION.md](DOCUMENTATION.md) - Полная документация API
- [CONTRIBUTING.md](CONTRIBUTING.md) - Как участвовать в развитии
- [README.md](README.md) - Основная информация о проекте

## 🎯 Основные компоненты

| Модуль | Описание |
|--------|---------|
| `converter.py` | Основной конвертер аудио в MIDI |
| `audio_processor.py` | Загрузка и предварительная обработка аудио |
| `pitch_detector.py` | Обнаружение высоты тона |
| `midi_generator.py` | Генерация MIDI файлов |
| `cli.py` | Интерфейс командной строки |

## 💡 Примеры

### Пример 1: Преобразование трека
```bash
bonk convert track.mp3 track_notation.mid
```

### Пример 2: С настройками
```bash
bonk convert vocal.wav vocal.mid --tempo 110 --min-duration 0.12
```

### Пример 3: Использование библиотеки
```python
from bonk import AudioToMidiConverter

converter = AudioToMidiConverter(sr=22050)
converter.convert(
    input_path="music.wav",
    output_path="notation.mid",
    tempo=120,
    min_duration=0.1
)
```

## 🧪 Тестирование

```bash
pytest tests/ -v
```

## 📝 Лицензия

MIT - см. [LICENSE](LICENSE)

## 🤝 Участие

Идеи? Баги? Pull requests приветствуются! Подробнее в [CONTRIBUTING.md](CONTRIBUTING.md)
