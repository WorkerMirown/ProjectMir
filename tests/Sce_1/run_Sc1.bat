@echo off
REM Проверка наличия аргумента base-url
IF "%1"=="" (
    echo Не указан base-url. Пример использования:
    echo run_SC1.bat test
    exit /b 1
)

REM Аргумент %1 передаем как base-url
set BASE_URL=%1

REM Переходим в папку с тестами (где лежит батник)
cd /d %~dp0

REM Указываем директорию для allure (относительно проекта)
set ALLURE_DIR=..\allure-results

REM Удаляем старые результаты allure
if exist %ALLURE_DIR% rmdir /s /q %ALLURE_DIR%

REM Запуск pytest только для текущей папки (Sce_1) с переданным base-url и headless
python -m pytest . --headless --base-url %BASE_URL%