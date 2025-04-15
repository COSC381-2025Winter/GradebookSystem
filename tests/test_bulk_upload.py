import pytest
import os
from instructor import Instructor
from data import is_valid_student_id, is_valid_grade, ROSTERS

def test_valid_student_id():
    """Test student ID validation"""
    # Valid cases
    assert is_valid_student_id("201") == True
    assert is_valid_student_id("999") == True
    
    # Invalid cases
    assert is_valid_student_id("20") == False    # Too short
    assert is_valid_student_id("2001") == False  # Too long
    assert is_valid_student_id("abc") == False   # Non-numeric
    assert is_valid_student_id("") == False      # Empty

def test_valid_grade():
    """Test grade validation"""
    # Valid letter grades
    assert is_valid_grade("A") == True
    assert is_valid_grade("B+") == True
    assert is_valid_grade("C-") == True
    
    # Valid numeric grades
    assert is_valid_grade("90") == True
    assert is_valid_grade("85.5") == True
    assert is_valid_grade("0") == True
    assert is_valid_grade("100") == True
    
    # Invalid cases
    assert is_valid_grade("X") == False     # Invalid letter
    assert is_valid_grade("101") == False   # Too high
    assert is_valid_grade("-5") == False    # Negative
    assert is_valid_grade("B++") == False   # Malformed
    assert is_valid_grade("") == False      # Empty

def test_bulk_upload_successful_rows():
    """Test successful rows in bulk upload"""
    instructor = Instructor(101)  # Valid instructor ID
    test_file = os.path.join(os.path.dirname(__file__), "sample_grades.csv")
    
    successes, errors = instructor.bulk_upload_grades("CS101", test_file)
    
    # Verify successful updates (first 6 rows in sample file are valid)
    assert len(successes) == 6
    assert any("201 to 90.5" in s for s in successes)
    assert any("203 to A" in s for s in successes)
    assert any("205 to 75.25" in s for s in successes)

def test_bulk_upload_errors():
    """Test error cases in bulk upload"""
    instructor = Instructor(101)
    test_file = os.path.join(os.path.dirname(__file__), "sample_grades.csv")
    
    successes, errors = instructor.bulk_upload_grades("CS101", test_file)
    
    # Verify errors (last 2 rows in sample file are invalid)
    assert len(errors) == 2
    assert "Invalid grade: 101" in errors
    assert "Invalid grade: X" in errors

def test_bulk_upload_enrollment_check():
    """Verify enrollment checking"""
    instructor = Instructor(101)
    test_file = os.path.join(os.path.dirname(__file__), "sample_grades.csv")
    
    # Test with unenrolled student (999 doesn't exist in ROSTERS)
    successes, errors = instructor.bulk_upload_grades("CS101", test_file)
    assert not any("999" in s for s in successes)