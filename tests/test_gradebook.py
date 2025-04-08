def test_add_negative_grade(capsys):
    from gradebook import Gradebook
    from instructor import Instructor

    gradebook = Gradebook()
    instructor = Instructor(1)  
    course_id = "CS101"         
    student_id = 1001           

    if not instructor.has_access(course_id):
        return

    gradebook.add_grade(instructor, course_id, student_id, -50)

    captured = capsys.readouterr()
    assert "Grade cannot be negative" in captured.out or "Error" in captured.out
