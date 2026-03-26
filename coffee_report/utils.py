"""Вспомогательные функции для форматирования отчетов."""

from typing import List

from coffee_report.models import StudentStats

try:
    from tabulate import tabulate
except ImportError:
    # Простое форматирование на случай, если tabulate не установлен
    def tabulate(data, headers="keys", tablefmt="grid"):
        """Простое форматирование таблицы как запасной вариант."""
        if not data:
            return ""

        if headers == "keys" and isinstance(data[0], dict):
            headers = list(data[0].keys())

        # Строим простую таблицу
        if headers:
            header_row = " | ".join(str(h) for h in headers)
            separator = "-+-".join("-" * len(str(h)) for h in headers)
            rows = [" | ".join(str(row.get(h, "")) for h in headers) for row in data]
            return f"{header_row}\n{separator}\n" + "\n".join(rows)

        return ""


def format_report(stats: List[StudentStats]) -> str:
    """Форматирует статистику по студентам в виде таблицы.

    Args:
        stats: Список объектов StudentStats

    Returns:
        Отформатированная строка с таблицей
    """
    # Если данных нет, выводим сообщение
    if not stats:
        return "Нет данных для отображения."

    # Подготавливаем данные для таблицы
    table_data = [
        {
            "Студент": stat.student,
            "Медианные траты на кофе": f"{stat.median_coffee_spent:.2f}",
        }
        for stat in stats
    ]

    # Форматируем в виде сетки для лучшей читаемости
    return tabulate(table_data, headers="keys", tablefmt="grid")
