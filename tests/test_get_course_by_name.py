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
    inputs = iter(["102", "light","CS102","x","","q"])    # test for regular input 

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    monkeypatch.setattr("getpass.getpass", lambda _: "javapro123")
   
    with pytest.raises(SystemExit):
        main()
    
    captured = capsys.readouterr()    
    assert "Logging out..." in captured.out