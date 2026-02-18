#!/bin/bash

# ============================================================================
# Bonk - Audio to MIDI Converter
# Скрипт для установки зависимостей и компиляции в exe-файл
# Для Linux и macOS
# ============================================================================

set -e  # Выход при первой ошибке

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  BONK - Audio to MIDI Converter - Setup & Build            ║"
echo "║  Установка зависимостей и компиляция                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функция для вывода ошибок
error_exit() {
    echo -e "${RED}❌ Ошибка: $1${NC}"
    exit 1
}

# Проверка Python
echo "[1/6] Проверка Python..."
if ! command -v python3 &> /dev/null; then
    error_exit "Python 3 не установлен. Пожалуйста, установите Python 3.8+"
fi

PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓${NC} Найден $PYTHON_VERSION"
echo ""

# Проверка и установка виртуального окружения
echo "[2/6] Проверка виртуального окружения..."
if [[ ! -d "venv" ]]; then
    echo "    Создание виртуального окружения..."
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Виртуальное окружение создано"
else
    echo -e "${GREEN}✓${NC} Виртуальное окружение уже существует"
fi

# Активация виртуального окружения
echo "    Активация виртуального окружения..."
source venv/bin/activate
echo -e "${GREEN}✓${NC} Окружение активировано"
echo ""

# Обновление pip
echo "[3/6] Обновление pip..."
python3 -m pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo -e "${GREEN}✓${NC} pip обновлён"
echo ""

# Установка зависимостей
echo "[4/6] Установка зависимостей (это может занять несколько минут)..."
pip install -r requirements.txt
if [[ $? -ne 0 ]]; then
    error_exit "Ошибка при установке зависимостей"
fi
echo -e "${GREEN}✓${NC} Зависимости установлены"
echo ""

# Проверка PyInstaller
echo "[5/6] Проверка PyInstaller..."
if ! command -v pyinstaller &> /dev/null; then
    error_exit "PyInstaller не установлен"
fi

PYINSTALLER_VERSION=$(pyinstaller --version 2>/dev/null || echo "6.0+")
echo -e "${GREEN}✓${NC} PyInstaller $PYINSTALLER_VERSION найден"
echo ""

# Компиляция в исполняемый файл
echo "[6/6] Компиляция в исполняемый файл..."
echo "      (это может занять 2-5 минут, пожалуйста подождите...)"
echo ""

# Определяем ОС
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    EXECUTABLE_NAME="bonk"
    SPEC_FILE="bonk.spec"
else
    # Linux
    EXECUTABLE_NAME="bonk"
    SPEC_FILE="bonk.spec"
fi

if [[ -f "$SPEC_FILE" ]]; then
    pyinstaller "$SPEC_FILE"
else
    pyinstaller --onefile --console \
                --name "$EXECUTABLE_NAME" \
                --distpath ./dist \
                --buildpath ./build \
                --spec-path ./ \
                bonk/__main__.py
fi

if [[ $? -ne 0 ]]; then
    error_exit "Ошибка при компиляции"
fi

echo ""

# Проверка результата
if [[ -f "dist/$EXECUTABLE_NAME" ]]; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                     ✅ УСПЕШНО!                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo -e "${GREEN}📦 Исполняемый файл создан:${NC} dist/$EXECUTABLE_NAME"
    echo ""
    
    # Получить размер файла
    if [[ "$OSTYPE" == "darwin"* ]]; then
        FILESIZE=$(stat -f%z "dist/$EXECUTABLE_NAME")
    else
        FILESIZE=$(stat -c%s "dist/$EXECUTABLE_NAME")
    fi
    
    echo "📊 Статистика сборки:"
    echo "   Размер: $((FILESIZE / 1024)) кБ"
    echo ""
    echo "🚀 Вы можете запустить $EXECUTABLE_NAME напрямую без установки Python!"
    echo ""
    echo "💡 Примеры использования:"
    echo "   ./dist/$EXECUTABLE_NAME convert song.mp3 output.mid"
    echo "   ./dist/$EXECUTABLE_NAME convert audio.wav output.mid --tempo 140"
    echo "   ./dist/$EXECUTABLE_NAME info audio.wav"
    echo ""
    echo "📁 Папка с файлом: dist/"
    echo ""
    echo "💡 Для удобства, сделайте файл исполняемым:"
    echo "   chmod +x dist/$EXECUTABLE_NAME"
    echo ""
    echo "   Добавьте в PATH или вызывайте с полным путём:"
    echo "   ./dist/$EXECUTABLE_NAME --help"
    echo ""
    
    # Сделаем файл исполняемым
    chmod +x "dist/$EXECUTABLE_NAME"
    echo -e "${GREEN}✓${NC} Файл сделан исполняемым"
    echo ""
    
else
    echo -e "${RED}❌ Ошибка: исполняемый файл не был создан${NC}"
    exit 1
fi

echo -e "${GREEN}✨ Сборка завершена!${NC}"
echo ""
