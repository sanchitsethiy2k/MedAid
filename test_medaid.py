from medaid import validate_name
from medaid import validate_bday
from medaid import validate_gender
import pytest

def test_validate_name():
    with pytest.raises(ValueError):
        validate_name("")

def test_validate_bday():
    with pytest.raises(ValueError):
        validate_bday("2007")
    with pytest.raises(ValueError):
        validate_bday("19-08")
    with pytest.raises(ValueError):
        validate_bday("19-09-2007")
    with pytest.raises(ValueError):
        validate_bday("19/00/2001")
    with pytest.raises(ValueError):
        validate_bday("29.10.2005")
    with pytest.raises(ValueError):
        validate_bday("First January 2007")
    with pytest.raises(ValueError):
        validate_bday("1st January 2007")

def test_validate_gender():
    with pytest.raises(ValueError):
        validate_gender("Man")
    with pytest.raises(ValueError):
        validate_gender("Woman")
