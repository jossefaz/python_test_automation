import enum
from dataclasses import dataclass
from pathlib import Path
from typing import List


def retrieve_users(db_connection):
    if db_connection.connected:
        return "All users"
    return "Not Connected to db"


def save_text_in_file(text: str, file_path: str):
    with open(file_path, "w+") as fp:
        fp.write(text)

class DummyDb:
    def __init__(self):
        self.connected = False

    def connect(self):
        self.connected = True


