from gradebook import Gradebook
import pytest

@pytest.fixture
def test_grades():
    gb = Gradebook()
    gb.grades = {
        "CS101": {
            "201": {"grade": "D", "timestamp": ""},
            "202": {"grade": "A", "timestamp": ""},
            "203": {"grade": "C", "timestamp": ""}
        }
    }
    return gb

@pytest.fixture
def empty_grades():
    gb = Gradebook()
    return gb

def test_asecending_list(test_grades):
    test_grades.sort_courses('a')

    assert test_grades.grades["CS101"] == {
        "202": {"grade": "A", "timestamp": ""},
        "203": {"grade": "C", "timestamp": ""},
        "201": {"grade": "D", "timestamp": ""}
    }
    
def test_decending_list(test_grades):
    test_grades.sort_courses('d')

    assert test_grades.grades["CS101"] == {
        "201": {"grade": "D", "timestamp": ""},
        "203": {"grade": "C", "timestamp": ""},
        "202": {"grade": "A", "timestamp": ""}
        }
    
def test_bad_input(test_grades, capsys):
    test_grades.sort_courses('q')

    captured = capsys.readouterr()

    assert "Please type either (a/d)" in captured.out

def test_empty_input(empty_grades, capsys):
    empty_grades.sort_courses('q')

    captured = capsys.readouterr()

    assert "Grades are empty. Please add a grade" in captured.out


            
           
            