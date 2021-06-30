import pytest
from ..app.main import retrieve_users


class DummyDb:
    def __init__(self):
        self.connected = False

    def connect(self):
        self.connected = True


@pytest.fixture
def db_connection():
    conn = DummyDb()
    conn.connect()
    return conn


# Notice the name of the parameter which is the exact same name of the fixture that we defined before
def test_retrieve_users(db_connection):
    assert retrieve_users(db_connection) == "All users"
