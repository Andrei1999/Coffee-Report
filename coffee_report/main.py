"""Интерфейс командной строки для отчета о кофе."""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from coffee_report.readers import read_multiple_files
from coffee_report.reporters import get_report_generator
from coffee_report.utils import format_report


def parse_arguments(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Разбирает аргументы командной строки.

    Args:
        args: Аргументы командной строки (None для sys.argv)

    Returns:
        Объект с разобранными аргументами
    """
    parser = argparse.ArgumentParser(
        description="Формирование отчетов из данных о потреблении кофе студентами."
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        type=Path,
        help="Пути к CSV-файлам с данными о потреблении кофе",
    )
    parser.add_argument(
        "--report",
        required=True,
        type=str,
        help="Тип отчета для формирования (например, median-coffee)",
    )

    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> int:
    """Главная точка входа в скрипт.

    Args:
        args: Аргументы командной строки (None для sys.argv)

    Returns:
        Код возврата (0 - успех, ненулевое значение - ошибка)
    """
    try:
        # Разбираем аргументы командной строки
        parsed_args = parse_arguments(args)

        # Читаем все CSV-файлы
        records = read_multiple_files(parsed_args.files)

        # Формируем отчет
        generator = get_report_generator(parsed_args.report, records)
        stats = generator.generate()

        # Выводим отчет в консоль
        print(format_report(stats))

        return 0

    except (FileNotFoundError, ValueError) as e:
        # Обрабатываем ожидаемые ошибки
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        # Обрабатываем прерывание от пользователя
        print("\nПрервано пользователем", file=sys.stderr)
        return 130
    except Exception as e:
        # Обрабатываем неожиданные ошибки
        print(f"Непредвиденная ошибка: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
