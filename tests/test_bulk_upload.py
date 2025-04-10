import pytest
import os
from instructor import Instructor
from data import is_valid_student_id, is_valid_grade

def test_valid_student_id():
    """Test student ID validation"""
    assert is_valid_student_id("123") == True
    assert is_valid_student_id("12") == False   # Too short
    assert is_valid_student_id("abc") == False  # Not digits

def test_valid_grade():
    """Test grade validation"""
    assert is_valid_grade("A") == True
    assert is_valid_grade("B+") == True
    assert is_valid_grade("X") == False  # Invalid grade

def test_bulk_upload():
    """Test full CSV upload using sample file"""
    instructor = Instructor(1)  # Test instructor ID
    
    # Get the path to the sample file in the tests folder
    test_file = os.path.join(os.path.dirname(__file__), "sample_grades.csv")
    
    successes, errors = instructor.bulk_upload_grades("COSC101", test_file)
    
    assert len(successes) == 3  # Should process all rows in sample file
    assert len(errors) == 0     # Should have no errors