import requests
from requests import Response


def check_user_credentials(user_credentials):
    return requests.post("https://mydomain/login", user_credentials)


def login(user_credentials):
    credentials = check_user_credentials(user_credentials)
    if not credentials:
        return 401
    return 200


def get_todo_from_rest():
    response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
    return response


# Return {'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': False}

def is_todo_completed(todo: Response):
    parsed_todo = todo.json()
    return parsed_todo["completed"]


def complete_todo():
    todo = get_todo_from_rest()
    if is_todo_completed(todo):
        return True
    return False
