def test_add_negative_grade(capsys):
    # Import necessary classes
    from gradebook import Gradebook
    from instructor import Instructor
    from data import ROSTERS

    # Use the first course and student from the data file
    course_id = list(ROSTERS.keys())[0]
    student_id = ROSTERS[course_id][0]

    # Create objects needed for testing
    gradebook = Gradebook()
    instructor = Instructor(1)

    # Skip the test if the instructor doesn't have access (safety check)
    if not instructor.has_access(course_id):
        return

    # Try to add a negative grade (UI logic should prevent this)
    gradebook.add_grade(instructor, course_id, student_id, -50)

    # Capture output and check for an error message
    captured = capsys.readouterr()
    assert "Grade cannot be negative" in captured.out
