"""Тесты для генераторов отчетов."""

import pytest
from coffee_report.models import CoffeeRecord
from coffee_report.reporters import (
    MedianCoffeeReport,
    ReportGenerator,
    get_report_generator,
)


def test_report_generator_abstract():
    """Тест, что базовый класс нельзя использовать напрямую."""
    records = []
    generator = ReportGenerator(records)

    with pytest.raises(NotImplementedError):
        generator.generate()


def test_median_coffee_report_single_student():
    """Тест вычисления медианы для одного студента."""
    records = [
        CoffeeRecord("Алексей", "2024-06-01", 450, 4.5, 12, "норм", "Математика"),
        CoffeeRecord("Алексей", "2024-06-02", 500, 4.0, 14, "устал", "Математика"),
        CoffeeRecord("Алексей", "2024-06-03", 550, 3.5, 16, "зомби", "Математика"),
    ]

    generator = MedianCoffeeReport(records)
    stats = generator.generate()

    assert len(stats) == 1
    assert stats[0].student == "Алексей"
    assert stats[0].median_coffee_spent == 500.0


def test_median_coffee_report_multiple_students():
    """Тест вычисления медианы для нескольких студентов с сортировкой."""
    records = [
        CoffeeRecord("Алексей", "2024-06-01", 450, 4.5, 12, "норм", "Математика"),
        CoffeeRecord("Алексей", "2024-06-02", 500, 4.0, 14, "устал", "Математика"),
        CoffeeRecord("Дарья", "2024-06-01", 200, 7.0, 6, "отл", "Математика"),
        CoffeeRecord("Дарья", "2024-06-02", 250, 6.5, 8, "норм", "Математика"),
        CoffeeRecord("Иван", "2024-06-01", 600, 3.0, 15, "зомби", "Математика"),
        CoffeeRecord("Иван", "2024-06-02", 650, 2.5, 17, "зомби", "Математика"),
    ]

    generator = MedianCoffeeReport(records)
    stats = generator.generate()

    assert len(stats) == 3
    assert stats[0].student == "Иван"
    assert stats[0].median_coffee_spent == 625.0
    assert stats[1].student == "Алексей"
    assert stats[1].median_coffee_spent == 475.0
    assert stats[2].student == "Дарья"
    assert stats[2].median_coffee_spent == 225.0


def test_median_coffee_report_even_number():
    """Тест вычисления медианы с четным количеством записей."""
    records = [
        CoffeeRecord("Мария", "2024-06-01", 100, 8.0, 3, "отл", "Математика"),
        CoffeeRecord("Мария", "2024-06-02", 200, 8.5, 2, "отл", "Математика"),
        CoffeeRecord("Мария", "2024-06-03", 300, 7.5, 4, "отл", "Математика"),
        CoffeeRecord("Мария", "2024-06-04", 400, 7.0, 5, "отл", "Математика"),
    ]

    generator = MedianCoffeeReport(records)
    stats = generator.generate()

    assert stats[0].median_coffee_spent == 250.0


def test_median_coffee_report_single_record():
    """Тест с одной записью для студента."""
    records = [
        CoffeeRecord("Петр", "2024-06-01", 300, 6.0, 8, "норм", "Математика"),
    ]

    generator = MedianCoffeeReport(records)
    stats = generator.generate()

    assert len(stats) == 1
    assert stats[0].median_coffee_spent == 300.0


def test_median_coffee_report_empty():
    """Тест вычисления медианы без записей."""
    generator = MedianCoffeeReport([])
    stats = generator.generate()
    assert stats == []


def test_median_coffee_report_same_median():
    """Тест студентов с одинаковой медианой."""
    records = [
        CoffeeRecord("Анна", "2024-06-01", 300, 6.0, 8, "норм", "Математика"),
        CoffeeRecord("Анна", "2024-06-02", 400, 5.5, 9, "норм", "Математика"),
        CoffeeRecord("Борис", "2024-06-01", 350, 5.0, 10, "норм", "Математика"),
        CoffeeRecord("Борис", "2024-06-02", 350, 5.0, 10, "норм", "Математика"),
    ]

    generator = MedianCoffeeReport(records)
    stats = generator.generate()

    # Медиана Анны = 350, Бориса = 350
    assert stats[0].median_coffee_spent == 350.0
    assert stats[1].median_coffee_spent == 350.0


def test_median_coffee_report_float_values():
    """Тест с дробными значениями трат."""
    records = [
        CoffeeRecord("Студент", "2024-06-01", 450, 4.5, 12, "норм", "Математика"),
        CoffeeRecord("Студент", "2024-06-02", 450, 4.0, 14, "устал", "Математика"),
    ]
    # coffee_spent - целые числа, но медиана может быть дробной при четном количестве
    # Здесь медиана 450.0

    generator = MedianCoffeeReport(records)
    stats = generator.generate()

    assert stats[0].median_coffee_spent == 450.0


def test_median_coffee_report_many_records():
    """Тест с большим количеством записей."""
    records = []
    student_name = "Студент"
    values = list(range(1, 101))  # 100 записей от 1 до 100

    for i, value in enumerate(values):
        records.append(
            CoffeeRecord(
                student_name,
                f"2024-06-{i + 1:02d}",
                value,
                5.0,
                10,
                "норм",
                "Математика",
            )
        )

    generator = MedianCoffeeReport(records)
    stats = generator.generate()

    # Медиана чисел от 1 до 100 = 50.5
    assert stats[0].median_coffee_spent == 50.5


def test_get_report_generator_valid():
    """Тест фабричной функции с корректным типом отчета."""
    records = []
    generator = get_report_generator("median-coffee", records)
    assert isinstance(generator, MedianCoffeeReport)


def test_get_report_generator_invalid():
    """Тест фабричной функции с некорректным типом отчета."""
    records = []

    with pytest.raises(ValueError) as exc_info:
        get_report_generator("invalid-report", records)
    assert "Неизвестный тип отчета" in str(exc_info.value)
    assert "invalid-report" in str(exc_info.value)


def test_get_report_generator_empty_string():
    """Тест фабричной функции с пустой строкой."""
    records = []

    with pytest.raises(ValueError):
        get_report_generator("", records)


def test_get_report_generator_case_sensitive():
    """Тест чувствительности к регистру."""
    records = []

    with pytest.raises(ValueError):
        get_report_generator("MEDIAN-COFFEE", records)
