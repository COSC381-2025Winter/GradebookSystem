import pytest
from main import main
from instructor import Instructor
import sys




@pytest.fixture(params=("Java Programming",))      #Acting a and Arranging
def test_get_course_code_by_name(request):
    instructor = Instructor(101)
    return instructor.get_course_code_by_name(request.param)


def test_func(test_get_course_code_by_name):        # Assert 
   assert test_get_course_code_by_name =="CS111"   # Should be "CS11" since  java programming has that course tage
    
    
    
def test_multiple_inputs(monkeypatch,capsys):
    # Simulating multiple inputs by using a list
    inputs = iter([102,"CS102","x","x","q"])    # test for regular input 
    
   
    
    
                
    
    
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
   
    
    with pytest.raises(SystemExit):
        main()

    
    captured = capsys.readouterr()
    
    print(captured.out)
    
    assert "[33mLogging out...\x1b[0m\n\n--- Gradebook System ---\n" in captured.out



    
    
    
    





