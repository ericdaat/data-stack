import pytest

from src import example_module



def test_basic():
    result = example_module.example_function()
    
    assert isinstance(result, str)
