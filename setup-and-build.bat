@echo off
REM ============================================================================
REM Bonk - Audio to MIDI Converter
REM Скрипт для установки зависимостей и компиляции в exe-файл
REM Для Windows
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  BONK - Audio to MIDI Converter - Setup ^& Build (Windows)  ║
echo ║  Установка зависимостей и компиляция в exe                ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Проверка Python
echo [1/5] Проверка Python...
set PYTHON_CMD=
set PYTHON_VERSION=

REM Сначала пробуем python
python --version >nul 2>&1
if errorlevel 0 (
    set PYTHON_CMD=python
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
)

REM Если python не сработал, пробуем python3
if "!PYTHON_CMD!"=="" (
    python3 --version >nul 2>&1
    if errorlevel 0 (
        set PYTHON_CMD=python3
        for /f "tokens=*" %%i in ('python3 --version 2^>^&1') do set PYTHON_VERSION=%%i
    )
)

REM Если всё равно не найдено, пробуем по пути AppData
if "!PYTHON_CMD!"=="" (
    if exist "%APPDATA%\..\Local\Programs\Python\Python311\python.exe" (
        set PYTHON_CMD=%APPDATA%\..\Local\Programs\Python\Python311\python.exe
        for /f "tokens=*" %%i in ('!PYTHON_CMD! --version 2^>^&1') do set PYTHON_VERSION=%%i
    )
)

if "!PYTHON_CMD!"=="" (
    echo ❌ Ошибка: Python не найден!
    echo.
    echo Решение:
    echo   1. Установите Python 3.8+ с https://www.python.org
    echo   2. При установке ОБЯЗАТЕЛЬНО выберите "Add Python to PATH"
    echo   3. Перезагрузите компьютер после установки
    echo   4. Откройте новое окно Command Prompt и запустите этот скрипт снова
    echo.
    echo Проверка:
    echo   - Откройте Command Prompt
    echo   - Введите: python --version
    echo   - Если Python найден, вы увидите версию
    echo.
    pause
    exit /b 1
)

echo ✓ Найден !PYTHON_VERSION!
echo   Использую: !PYTHON_CMD!
echo.

REM Обновление pip
echo [2/5] Обновление pip...
!PYTHON_CMD! -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo ❌ Ошибка при обновлении pip
    pause
    exit /b 1
)
echo ✓ pip обновлён
echo.

REM Установка зависимостей
echo [3/5] Установка зависимостей (это может занять несколько минут)...
!PYTHON_CMD! -m pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Ошибка при установке зависимостей
    pause
    exit /b 1
)
echo ✓ Зависимости установлены
echo.

REM Проверка что PyInstaller установлен
echo [4/5] Проверка PyInstaller...
!PYTHON_CMD! -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Ошибка: PyInstaller не установлен
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('!PYTHON_CMD! -m PyInstaller --version 2^>^&1') do set PYINSTALLER_VERSION=%%i
echo ✓ PyInstaller !PYINSTALLER_VERSION! найден
echo.

REM Компиляция в exe
echo [5/5] Компиляция в exe-файл...
echo      (это может занять 2-5 минут, пожалуйста подождите...)
echo.

if exist "bonk.spec" (
    !PYTHON_CMD! -m PyInstaller bonk.spec
) else (
    !PYTHON_CMD! -m PyInstaller --onefile --name bonk --distpath ./dist --buildpath ./build ^
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
