"""Тесты для читалок CSV-файлов."""

import tempfile
from pathlib import Path
import pytest
from coffee_report.readers import CSVReader, read_multiple_files


def test_csv_reader_reads_valid_file():
    """Тест чтения валидного CSV-файла."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f:
        f.write("student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n")
        f.write("Алексей Смирнов,2024-06-01,450,4.5,12,норм,Математика\n")
        f.write("Алексей Смирнов,2024-06-02,500,4.0,14,устал,Математика\n")
        temp_path = Path(f.name)

    try:
        reader = CSVReader(temp_path)
        records = reader.read()

        assert len(records) == 2
        assert records[0].student == "Алексей Смирнов"
        assert records[0].coffee_spent == 450
        assert records[0].sleep_hours == 4.5
        assert records[0].study_hours == 12
        assert records[0].mood == "норм"
        assert records[0].exam == "Математика"
        assert records[0].date == "2024-06-01"

        assert records[1].coffee_spent == 500
    finally:
        temp_path.unlink(missing_ok=True)


def test_csv_reader_reads_empty_file():
    """Тест чтения пустого CSV-файла."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f:
        f.write("student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n")
        temp_path = Path(f.name)

    try:
        reader = CSVReader(temp_path)
        records = reader.read()

        assert len(records) == 0
    finally:
        temp_path.unlink(missing_ok=True)


def test_csv_reader_reads_large_numbers():
    """Тест чтения больших чисел."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f:
        f.write("student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n")
        f.write("Студент,2024-06-01,999999,24.0,24,отл,Математика\n")
        temp_path = Path(f.name)

    try:
        reader = CSVReader(temp_path)
        records = reader.read()

        assert records[0].coffee_spent == 999999
        assert records[0].sleep_hours == 24.0
        assert records[0].study_hours == 24
    finally:
        temp_path.unlink(missing_ok=True)


def test_csv_reader_negative_values():
    """Тест чтения отрицательных значений (хотя это странно для кофе)."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f:
        f.write("student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n")
        f.write("Студент,2024-06-01,-100,-5.5,-10,плохо,Математика\n")
        temp_path = Path(f.name)

    try:
        reader = CSVReader(temp_path)
        records = reader.read()

        assert records[0].coffee_spent == -100
        assert records[0].sleep_hours == -5.5
        assert records[0].study_hours == -10
    finally:
        temp_path.unlink(missing_ok=True)


def test_csv_reader_file_not_found():
    """Тест чтения несуществующего файла."""
    reader = CSVReader(Path("/nonexistent/file.csv"))

    with pytest.raises(FileNotFoundError) as exc_info:
        reader.read()
    assert "Файл не найден" in str(exc_info.value)


def test_csv_reader_invalid_format():
    """Тест чтения файла с неверным форматом."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f:
        f.write("wrong,header,format\n")
        f.write("data1,data2,data3\n")
        temp_path = Path(f.name)

    try:
        reader = CSVReader(temp_path)
        with pytest.raises(ValueError) as exc_info:
            reader.read()
        assert "Неверный формат CSV" in str(exc_info.value)
    finally:
        temp_path.unlink(missing_ok=True)


def test_csv_reader_missing_columns():
    """Тест чтения файла с отсутствующими колонками."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f:
        f.write("student,date,coffee_spent\n")
        f.write("Алексей,2024-06-01,450\n")
        temp_path = Path(f.name)

    try:
        reader = CSVReader(temp_path)
        with pytest.raises(ValueError):
            reader.read()
    finally:
        temp_path.unlink(missing_ok=True)


def test_read_multiple_files():
    """Тест чтения нескольких файлов."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f1:
        f1.write("student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n")
        f1.write("Иван,2024-06-01,600,3.0,15,зомби,Математика\n")
        temp_path1 = Path(f1.name)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f2:
        f2.write("student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n")
        f2.write("Мария,2024-06-01,100,8.0,3,отл,Математика\n")
        temp_path2 = Path(f2.name)

    try:
        records = read_multiple_files([temp_path1, temp_path2])
        assert len(records) == 2
        assert records[0].student == "Иван"
        assert records[1].student == "Мария"
    finally:
        temp_path1.unlink(missing_ok=True)
        temp_path2.unlink(missing_ok=True)


def test_read_multiple_files_three_files():
    """Тест чтения трех файлов."""
    temp_paths = []
    try:
        for i in range(3):
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False, encoding="utf-8"
            ) as f:
                f.write("student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n")
                f.write(
                    f"Студент{i},2024-06-01,{100 * (i + 1)},5.0,10,норм,Математика\n"
                )
                temp_paths.append(Path(f.name))

        records = read_multiple_files(temp_paths)
        assert len(records) == 3
        assert records[0].coffee_spent == 100
        assert records[1].coffee_spent == 200
        assert records[2].coffee_spent == 300
    finally:
        for path in temp_paths:
            path.unlink(missing_ok=True)


def test_read_multiple_files_with_error():
    """Тест чтения нескольких файлов с ошибкой в одном из них."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, encoding="utf-8"
    ) as f:
        f.write("student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n")
        f.write("Иван,2024-06-01,600,3.0,15,зомби,Математика\n")
        temp_path = Path(f.name)

    try:
        with pytest.raises(ValueError):
            read_multiple_files([temp_path, Path("/nonexistent.csv")])
    finally:
        temp_path.unlink(missing_ok=True)


def test_read_multiple_files_all_invalid():
    """Тест чтения нескольких невалидных файлов."""
    with pytest.raises(ValueError):
        read_multiple_files([Path("/nonexistent1.csv"), Path("/nonexistent2.csv")])
