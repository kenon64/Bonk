# 📦 Сборка Bonk - Скрипты компиляции

Инструкции по использованию скриптов для установки зависимостей и создания exe-файла.

## 🚀 Быстрый старт

### Windows

1. **Откройте CMD или PowerShell в папке проекта**
   ```
   cd /path/to/Bonk
   ```

2. **Запустите скрипт сборки**
   ```
   setup-and-build.bat
   ```

   Или двойной клик на `setup-and-build.bat`

3. **Ждите завершения**
   - Установка зависимостей: 2-3 минуты
   - Компиляция: 2-5 минут

4. **Найдите exe-файл**
   ```
   dist/bonk.exe
   ```

### Linux / macOS

1. **Откройте терминал в папке проекта**
   ```bash
   cd /path/to/Bonk
   ```

2. **Выполните разрешение на выполнение (если требуется)**
   ```bash
   chmod +x setup-and-build.sh
   ```

3. **Запустите скрипт сборки**
   ```bash
   ./setup-and-build.sh
   ```

4. **Ждите завершения** (4-8 минут)

5. **Найдите исполняемый файл**
   ```bash
   dist/bonk
   ```

## 📋 Что делают скрипты?

### Windows (setup-and-build.bat)

```
1. Проверка Python ✓
2. Обновление pip ✓
3. Установка зависимостей из requirements.txt ✓
4. Проверка PyInstaller ✓
5. Компиляция в exe-файл ✓
```

### Linux / macOS (setup-and-build.sh)

```
1. Проверка Python 3 ✓
2. Создание виртуального окружения (venv) ✓
3. Обновление pip ✓
4. Установка зависимостей ✓
5. Проверка PyInstaller ✓
6. Компиляция в исполняемый файл ✓
```

## 🎯 Требования

### Windows
- Python 3.8+ (скачать с https://www.python.org)
- FFmpeg (опционально, для MP3 поддержки)
- Минимум 2 ГБ свободного места на диске

### Linux / macOS
- Python 3.8+
- pip
- На macOS: Xcode Command Line Tools

### Установка необходимого ПО

#### Windows - FFmpeg (опционально)
```
1. Скачать: https://ffmpeg.org/download.html
2. Распаковать в папку
3. Добавить в PATH или использовать полный путь
```

#### Ubuntu / Debian - FFmpeg
```bash
sudo apt-get update
sudo apt-get install ffmpeg python3-dev
```

#### macOS - FFmpeg
```bash
brew install ffmpeg
```

## 📊 Процесс сборки

### Этап 1: Проверка окружения
- ✓ Проверяется наличие Python
- ✓ Проверяется pip
- ✓ Создаётся/активируется виртуальное окружение (Linux/macOS)

### Этап 2: Установка зависимостей
**Основные библиотеки:**
- librosa — анализ аудио
- numpy, scipy — числовые вычисления
- pretty_midi — работа с MIDI
- click — CLI интерфейс
- pyinstaller — компиляция

**Время: 2-3 минуты** (зависит от Интернета)

### Этап 3: Компиляция
- PyInstaller анализирует код
- Упаковывает все зависимости
- Создаёт однофайловый exe/исполняемый файл

**Время: 2-5 минут**

## 💾 Результат

### Windows
```
dist/
└── bonk.exe (≈150-200 МБ)
```

### Linux / macOS
```
dist/
└── bonk (≈150-200 МБ)
```

Файл полностью независим и не требует установки Python!

## 🎮 Использование скомпилированного файла

### Windows
```cmd
cd dist
bonk.exe convert song.mp3 output.mid
bonk.exe convert audio.wav out.mid --tempo 140
bonk.exe info audio.wav
```

### Linux / macOS
```bash
./dist/bonk convert song.mp3 output.mid
./dist/bonk convert audio.wav out.mid --tempo 140
./dist/bonk info audio.wav
```

### Добавить в PATH (Linux/macOS)
```bash
export PATH="$PATH:$(pwd)/dist"
bonk convert song.mp3 output.mid
```

## ⚠️ Возможные проблемы и решения

### Проблема: Python не найден
```
❌ Python не установлен или не добавлен в PATH
```

**Решение:**
1. Скачать Python с https://www.python.org
2. При установке выбрать "Add Python to PATH"
3. Перезагрузить CMD/терминал

### Проблема: PyInstaller ошибка
```
❌ Ошибка при компиляции
```

**Решение:**
```bash
# Windows
pip install --upgrade pyinstaller

# Linux/macOS
pip3 install --upgrade pyinstaller
```

### Проблема: Не хватает места на диске
```
❌ Ошибка при компиляции
```

**Решение:**
1. Очистить диск (требуется ≈500 МБ для сборки)
2. Использовать временную папку на другом диске

### Проблема: Антивирус блокирует exe
```
⚠️ Антивирус может помечить exe как угрозу
```

**Решение:**
1. Добавить в исключения антивируса
2. Или скомпилировать самостоятельно
3. Подписать exe-файл сертификатом

### Проблема: FFmpeg необходим
```
⚠️ Ошибка при загрузке MP3: нужен FFmpeg
```

**Решение:**
- Установить FFmpeg (см. выше)
- Или использовать WAV/OGG формат вместо MP3

## 🔧 Ручная сборка (продвинутые пользователи)

Если автоматические скрипты не работают:

```bash
# 1. Установить зависимости
pip install -r requirements.txt

# 2. Компилировать вручную
pyinstaller bonk.spec

# 3. Результат в dist/bonk.exe
```

## 📝 Кастомизация сборки

Отредактируйте `bonk.spec` для изменения:
- **Имя программы:** измените `name='bonk'`
- **Консоль/GUI:** измените `console=True/False`
- **Иконка:** добавьте `icon='path/to/icon.ico'`
- **Скрытые импорты:** пополните `hiddenimports=[]`

## 🔐 Безопасность

**Скомпилированный файл:**
- ✓ Полностью независим
- ✓ Не требует Python
- ✓ Исходный код упакован (но не зашифрован)
- ✓ Можно распространять без ограничений (MIT лицензия)

## 📚 Дополнительная информация

- [PyInstaller документация](https://pyinstaller.org/)
- [Python упаковка](https://packaging.python.org/)
- [Bonk документация](DOCUMENTATION.md)

## 🆘 Помощь и поддержка

Если возникли проблемы:

1. **Проверьте лог компиляции** (в терминале вверху)
2. **Прочитайте сообщение об ошибке**
3. **Создайте issue** на GitHub с полным текстом ошибки

## 📞 Контакты

- GitHub: [kenon64/Bonk](https://github.com/kenon64/Bonk)
- Email: [ваш email]

---

✨ **Успешной сборки!** 🎵
