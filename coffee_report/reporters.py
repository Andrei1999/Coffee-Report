"""Логика формирования отчетов."""

from collections import defaultdict
from statistics import median
from typing import Dict, List

from coffee_report.models import CoffeeRecord, StudentStats


class ReportGenerator:
    """Базовый класс для генераторов отчетов."""

    def __init__(self, records: List[CoffeeRecord]) -> None:
        """Инициализирует генератор с данными.

        Args:
            records: Список записей о потреблении кофе
        """
        self.records = records

    def generate(self) -> List[StudentStats]:
        """Формирует отчет. Должен быть переопределен в дочерних классах.

        Returns:
            Список объектов StudentStats
        """
        raise NotImplementedError


class MedianCoffeeReport(ReportGenerator):
    """Отчет о медианных тратах на кофе по каждому студенту."""

    def generate(self) -> List[StudentStats]:
        """Вычисляет медианную сумму трат на кофе для каждого студента.

        Returns:
            Список StudentStats, отсортированный по убыванию медианных трат
        """
        # Собираем все траты по студентам
        coffee_by_student: Dict[str, List[int]] = defaultdict(list)

        for record in self.records:
            coffee_by_student[record.student].append(record.coffee_spent)

        # Вычисляем медиану для каждого студента
        stats: List[StudentStats] = []
        for student, coffee_spent_list in coffee_by_student.items():
            median_value = median(coffee_spent_list)
            stats.append(
                StudentStats(student=student, median_coffee_spent=median_value)
            )

        # Сортируем по убыванию медианных трат
        stats.sort(key=lambda x: x.median_coffee_spent, reverse=True)

        return stats


def get_report_generator(
    report_type: str, records: List[CoffeeRecord]
) -> ReportGenerator:
    """Фабричная функция для получения генератора отчета.

    Args:
        report_type: Тип отчета для формирования
        records: Список записей о потреблении кофе

    Returns:
        Экземпляр генератора отчета

    Raises:
        ValueError: Если тип отчета неизвестен
    """
    # Словарь доступных типов отчетов
    report_types = {
        "median-coffee": MedianCoffeeReport,
    }

    # Проверяем, существует ли запрошенный тип отчета
    if report_type not in report_types:
        raise ValueError(
            f"Неизвестный тип отчета: {report_type}. "
            f"Доступные отчеты: {', '.join(report_types.keys())}"
        )

    # Возвращаем экземпляр нужного генератора
    return report_types[report_type](records)
