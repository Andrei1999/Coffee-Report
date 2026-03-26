# Coffee-Report

Скрипт для обработки CSV-файлов с данными о потреблении кофе студентами во время сессии.

## Примеры запуска

```cmd
# Обработка одного файла
python -m coffee_report.main --files csv/math.csv --report median-coffee

# Обработка нескольких файлов
python -m coffee_report.main --files csv/math.csv csv/physics.csv csv/programming.csv --report median-coffee

# скриншоты запуска скрипта находятся в директории screenshots
