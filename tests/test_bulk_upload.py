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

def test_bulk_upload(tmp_path):
    """Test full CSV upload"""
    # Create a test CSV file
    test_file = os.path.join(tmp_path, "test.csv")
    with open(test_file, 'w') as f:
        f.write("student_id,grade\n123,A\n456,B+")
    
    # Test the upload
    instructor = Instructor(1)  # Test instructor ID
    successes, errors = instructor.bulk_upload_grades("COSC101", test_file)
    
    assert len(successes) == 2  # Should process 2 valid rows
    assert len(errors) == 0     # Should have no errors