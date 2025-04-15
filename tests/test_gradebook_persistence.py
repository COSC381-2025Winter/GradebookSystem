import os
import csv
import datetime
import pytest
from gradebook import Gradebook
from io import StringIO

def test_grade_is_saved_and_loaded(tmp_path):
    # Arrange
    csv_path = tmp_path / "grades.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["course_id", "student_id", "grade", "timestamp"])
        writer.writeheader()
        writer.writerow({
            "course_id": "CS101",
            "student_id": "201",
            "grade": "95.0",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    gb = Gradebook(file_path=csv_path)

    # Assert
    assert "CS101" in gb.grades
    assert 201 in gb.grades["CS101"]
    assert gb.grades["CS101"][201]["grade"] == 95.0

def test_empty_csv_shows_empty_message(tmp_path, monkeypatch, capsys):
    # Arrange
    empty_csv_path = tmp_path / "test_grades_empty.csv"
    with open(empty_csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["course_id", "student_id", "grade", "timestamp"])

    gb = Gradebook(file_path=empty_csv_path)
    monkeypatch.setattr('builtins.input', lambda _: '')

    # Act
    gb.sort_courses("a")
    captured = capsys.readouterr()

    # Assert
    assert "Grades are empty. Please add a grade" in captured.out
