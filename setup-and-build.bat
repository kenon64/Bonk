@echo off
REM ============================================================================
REM Bonk - Audio to MIDI Converter
REM Скрипт для установки зависимостей и компиляции в exe-файл
REM Для Windows
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  BONK - Audio to MIDI Converter - Setup & Build (Windows)  ║
echo ║  Установка зависимостей и компиляция в exe                ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Проверка Python
echo [1/5] Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Ошибка: Python не установлен или не добавлен в PATH
    echo    Пожалуйста, установите Python 3.8+ с https://www.python.org
    echo    При установке выберите опцию "Add Python to PATH"
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ Найден %PYTHON_VERSION%
echo.

REM Обновление pip
echo [2/5] Обновление pip...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo ❌ Ошибка при обновлении pip
    pause
    exit /b 1
)
echo ✓ pip обновлён
echo.

REM Установка зависимостей
echo [3/5] Установка зависимостей (это может занять несколько минут)...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Ошибка при установке зависимостей
    pause
    exit /b 1
)
echo ✓ Зависимости установлены
echo.

REM Проверка что PyInstaller установлен
echo [4/5] Проверка PyInstaller...
pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Ошибка: PyInstaller не установлен
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('pyinstaller --version') do set PYINSTALLER_VERSION=%%i
echo ✓ PyInstaller %PYINSTALLER_VERSION% найден
echo.

REM Компиляция в exe
echo [5/5] Компиляция в exe-файл...
echo      (это может занять 2-5 минут, пожалуйста подождите...)
echo.

if exist "bonk.spec" (
    pyinstaller bonk.spec
) else (
    pyinstaller --onefile --windowed --icon=./bonk/assets/icon.ico ^
                --name bonk --distpath ./dist --buildpath ./build ^
                --spec-path ./ bonk/__main__.py
)

if errorlevel 1 (
    echo ❌ Ошибка при компиляции
    pause
    exit /b 1
)
echo.

REM Проверка результата
if exist "dist\bonk.exe" (
    echo.
    echo ╔════════════════════════════════════════════════════════════╗
    echo ║                     ✅ УСПЕШНО!                            ║
    echo ╚════════════════════════════════════════════════════════════╝
    echo.
    echo 📦 exe-файл создан: dist\bonk.exe
    echo.
    echo 📊 Статистика сборки:
    for /f %%A in ('dir /b dist\bonk.exe') do set FILESIZE=%%~zA
    echo    Размер: %FILESIZE% байт
    echo.
    echo 🚀 Вы можете запустить bonk.exe напрямую без установки Python!
    echo.
    echo 💡 Примеры использования:
    echo    bonk.exe convert song.mp3 output.mid
    echo    bonk.exe convert audio.wav output.mid --tempo 140
    echo    bonk.exe info audio.wav
    echo.
    echo 📁 Папка с файлом: dist\
    echo.
    echo Можно двигать bonk.exe в любое место на компьютере.
    echo.
    pause
) else (
    echo ❌ Ошибка: exe-файл не был создан
    pause
    exit /b 1
)
