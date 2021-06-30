import requests


def check_user_credentials(user_credentials):
    return requests.post("https://mydomain/login", user_credentials)


def login(user_credentials):
    credentials = check_user_credentials(user_credentials)
    if not credentials:
        return 401
    return 200
