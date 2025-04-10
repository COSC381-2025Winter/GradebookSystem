from main import main
import pytest



def test_quitmsg():

    with pytest.raises(SystemExit) as exitInfo:
        main()