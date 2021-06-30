from pathlib import Path


def retrieve_users(db_connection):
    if db_connection.connected:
        return "All users"
    return "Not Connected to db"


def save_text_in_file(text: str, file_path: str):
    with open(file_path, "w+") as fp:
            fp.write(text)
