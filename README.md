# Coffee-Report

Скрипт для обработки CSV-файлов с данными о потреблении кофе студентами во время сессии.

## Примеры запуска

```cmd
# Обработка одного файла
python -m coffee_report.main --files csv/math.csv --report median-coffee

<img width="979" height="638" alt="image" src="https://github.com/user-attachments/assets/4a84deb2-a4e9-443b-89ae-284b592fee60" />



# Обработка нескольких файлов
python -m coffee_report.main --files csv/math.csv csv/physics.csv csv/programming.csv --report median-coffee

<img width="1103" height="775" alt="image" src="https://github.com/user-attachments/assets/0dca5584-6e3b-47df-bf7c-0367f98b77e4" />
