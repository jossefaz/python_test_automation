import os.path

import pytest
from ..app.main import retrieve_users, save_text_in_file


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


def test_write_text_to_file(tmpdir):
    file_name = "dummy_file.txt"
    file_path = os.path.join(tmpdir, file_name)
    text_to_write = "Hello World"
    save_text_in_file(text_to_write, file_path)
    with open(file_path, 'r') as fp:
        assert fp.readline() == text_to_write
