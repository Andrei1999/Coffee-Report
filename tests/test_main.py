"""Тесты для интерфейса командной строки."""

import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from coffee_report.main import main, parse_arguments


def test_parse_arguments_valid():
    """Тест разбора корректных аргументов."""
    test_args = [
        "script.py",
        "--files",
        "file1.csv",
        "file2.csv",
        "--report",
        "median-coffee",
    ]

    with patch.object(sys, "argv", test_args):
        args = parse_arguments()

        assert len(args.files) == 2
        assert args.files[0] == Path("file1.csv")
        assert args.files[1] == Path("file2.csv")
        assert args.report == "median-coffee"


def test_parse_arguments_single_file():
    """Тест разбора с одним файлом."""
    test_args = ["script.py", "--files", "file.csv", "--report", "median-coffee"]

    with patch.object(sys, "argv", test_args):
        args = parse_arguments()

        assert len(args.files) == 1
        assert args.files[0] == Path("file.csv")


def test_parse_arguments_missing_files():
    """Тест разбора аргументов без указания файлов."""
    test_args = ["script.py", "--report", "median-coffee"]

    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            parse_arguments()


def test_parse_arguments_missing_report():
    """Тест разбора аргументов без указания отчета."""
    test_args = ["script.py", "--files", "file.csv"]

    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            parse_arguments()


def test_parse_arguments_no_args():
    """Тест разбора без аргументов."""
    test_args = ["script.py"]

    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            parse_arguments()


def test_parse_arguments_extra_args():
    """Тест разбора с дополнительными неизвестными аргументами.

    Проверяем, что при передаче неизвестных аргументов программа корректно завершается с ошибкой.
    """
    test_args = [
        "script.py",
        "--files",
        "file.csv",
        "--report",
        "median-coffee",
        "--extra",
        "value",
    ]

    with patch.object(sys, "argv", test_args):
        # Ожидаем, что argparse вызовет SystemExit при неизвестных аргументах
        with pytest.raises(SystemExit) as exc_info:
            parse_arguments()
        # Проверяем, что код ошибки ненулевой
        assert exc_info.value.code != 0


def test_main_success():
    """Тест успешного выполнения основной функции."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f:
        f.write("student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n")
        f.write("Алексей,2024-06-01,450,4.5,12,норм,Математика\n")
        f.write("Алексей,2024-06-02,500,4.0,14,устал,Математика\n")
        temp_path = Path(f.name)

    try:
        exit_code = main(["--files", str(temp_path), "--report", "median-coffee"])
        assert exit_code == 0
    finally:
        temp_path.unlink(missing_ok=True)


def test_main_multiple_files_success():
    """Тест успешного выполнения с несколькими файлами."""
    temp_paths = []
    try:
        for i in range(2):
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False, encoding="utf-8"
            ) as f:
                f.write("student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n")
                f.write(
                    f"Студент{i},2024-06-01,{100 * (i + 1)},5.0,10,норм,Математика\n"
                )
                temp_paths.append(Path(f.name))

        args = (
            ["--files"] + [str(p) for p in temp_paths] + ["--report", "median-coffee"]
        )
        exit_code = main(args)
        assert exit_code == 0
    finally:
        for path in temp_paths:
            path.unlink(missing_ok=True)


def test_main_file_not_found():
    """Тест основной функции с несуществующим файлом."""
    exit_code = main(["--files", "/nonexistent.csv", "--report", "median-coffee"])
    assert exit_code == 1


def test_main_invalid_report():
    """Тест основной функции с неизвестным типом отчета."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f:
        f.write("student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n")
        f.write("Алексей,2024-06-01,450,4.5,12,норм,Математика\n")
        temp_path = Path(f.name)

    try:
        exit_code = main(["--files", str(temp_path), "--report", "invalid-report"])
        assert exit_code == 1
    finally:
        temp_path.unlink(missing_ok=True)


def test_main_empty_file():
    """Тест основной функции с пустым файлом."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f:
        f.write("student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n")
        temp_path = Path(f.name)

    try:
        exit_code = main(["--files", str(temp_path), "--report", "median-coffee"])
        assert exit_code == 0
    finally:
        temp_path.unlink(missing_ok=True)


def test_main_file_with_invalid_data():
    """Тест основной функции с файлом, содержащим невалидные данные."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f:
        f.write("student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n")
        f.write("Алексей,2024-06-01,not_a_number,4.5,12,норм,Математика\n")
        temp_path = Path(f.name)

    try:
        exit_code = main(["--files", str(temp_path), "--report", "median-coffee"])
        assert exit_code == 1
    finally:
        temp_path.unlink(missing_ok=True)


@patch("builtins.print")
def test_main_output_format(mock_print):
    """Тест формата вывода."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f:
        f.write("student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n")
        f.write("Алексей,2024-06-01,450,4.5,12,норм,Математика\n")
        temp_path = Path(f.name)

    try:
        exit_code = main(["--files", str(temp_path), "--report", "median-coffee"])
        assert exit_code == 0
        # Проверяем, что print был вызван
        assert mock_print.called
    finally:
        temp_path.unlink(missing_ok=True)
