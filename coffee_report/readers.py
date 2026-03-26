"""Утилиты для чтения CSV-файлов."""

import csv
from pathlib import Path
from typing import List

from coffee_report.models import CoffeeRecord


class CSVReader:
    """Читает данные о потреблении кофе из CSV-файла."""

    def __init__(self, file_path: Path) -> None:
        """Инициализирует читалку с путем к файлу.

        Args:
            file_path: Путь к CSV-файлу
        """
        self.file_path = file_path

    def read(self) -> List[CoffeeRecord]:
        """Читает CSV-файл и возвращает список записей.

        Returns:
            Список объектов CoffeeRecord

        Raises:
            FileNotFoundError: Если файл не существует
            ValueError: Если CSV-файл имеет неверный формат
        """
        # Проверяем существование файла
        if not self.file_path.exists():
            raise FileNotFoundError(f"Файл не найден: {self.file_path}")

        records: List[CoffeeRecord] = []

        # Открываем файл с правильной кодировкой для русских символов
        with open(self.file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            # Проверяем наличие всех необходимых колонок
            expected_fields = {
                "student",
                "date",
                "coffee_spent",
                "sleep_hours",
                "study_hours",
                "mood",
                "exam",
            }
            if not expected_fields.issubset(set(reader.fieldnames or [])):
                raise ValueError(
                    f"Неверный формат CSV в файле {self.file_path}. "
                    f"Ожидаются колонки: {expected_fields}"
                )

            # Читаем строки и преобразуем типы данных
            for row in reader:
                records.append(
                    CoffeeRecord(
                        student=row["student"],
                        date=row["date"],
                        coffee_spent=int(row["coffee_spent"]),
                        sleep_hours=float(row["sleep_hours"]),
                        study_hours=int(row["study_hours"]),
                        mood=row["mood"],
                        exam=row["exam"],
                    )
                )

        return records


def read_multiple_files(file_paths: List[Path]) -> List[CoffeeRecord]:
    """Читает несколько CSV-файлов и объединяет записи.

    Args:
        file_paths: Список путей к CSV-файлам

    Returns:
        Объединенный список объектов CoffeeRecord из всех файлов

    Raises:
        ValueError: Если при чтении какого-либо файла произошла ошибка
    """
    all_records: List[CoffeeRecord] = []
    errors: List[str] = []

    # Последовательно читаем каждый файл
    for file_path in file_paths:
        try:
            reader = CSVReader(file_path)
            records = reader.read()
            all_records.extend(records)
        except (FileNotFoundError, ValueError) as e:
            errors.append(str(e))

    # Если были ошибки, выбрасываем исключение со всеми сообщениями
    if errors:
        raise ValueError("\n".join(errors))

    return all_records
