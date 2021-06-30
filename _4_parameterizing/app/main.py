def log_in(username: str, password: str) -> int:
    if username == "john" and password == "supersecret":
        return 200
    # Return 401 unauthorized
    return 401
