from ..app.main import add

def test_add_num():
    assert add(1,2) == 3

def test_add_str():
    assert add("hello ", "world") == "hello world"

class TestMain:
    def test_add_num(self):
        raise
        assert add(1, 2) == 3

    def test_add_str(self):
        assert add("hello ", "world") == "hello world"
