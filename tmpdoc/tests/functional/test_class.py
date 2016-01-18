class TestClass:

    def test_one(self):
        x = "this"
        assert 'h' in x

    def test_two(self):
        self.x = "check"
        assert hasattr(self, 'x')
