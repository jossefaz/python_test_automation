import pytest
from ..app.main import log_in


@pytest.mark.parametrize("username, password, expected_status_code",
                          [("john", "supersecret", 200),
                           ("john", "wrongpassword", 401),
                           ("wronguser", "supersecret", 401)])
def test_login(username, password, expected_status_code):
    assert log_in(username,password) == expected_status_code