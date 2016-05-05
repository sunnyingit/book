import pytest

class TestPytest():

    @pytest.mark.parametrize("a,b,c", [(1,2,3), (3,4,5)])
    def test_paramize(self, a,b,c):
        print a,b,c
        assert 0
