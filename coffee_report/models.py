"""Модели данных для отчетов о потреблении кофе."""

from dataclasses import dataclass


@dataclass
class CoffeeRecord:
    """Запись о потреблении кофе."""

    student: str  # ФИО студента
    date: str  # Дата записи
    coffee_spent: int  # Потрачено на кофе (в рублях)
    sleep_hours: float  # Количество часов сна
    study_hours: int  # Количество часов учебы
    mood: str  # Настроение
    exam: str  # Название экзамена


@dataclass
class StudentStats:
    """Статистика по студенту."""

    student: str  # ФИО студента
    median_coffee_spent: float  # Медианная сумма трат на кофе
