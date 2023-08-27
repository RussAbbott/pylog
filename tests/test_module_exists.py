import pytest
import importlib.util as u
def test_pylog_exists():
    spec=u.find_spec("pylog")
    assert(spec)

def test_pylog_loads():
    import pylog 
    assert(pylog)