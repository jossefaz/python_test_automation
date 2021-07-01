from unittest import mock

import pytest
from ..app.main import login, complete_todo
from ..app import main as main_module


def fake_check_credentials(user_credentials):
    if user_credentials["username"] == "existing_user" \
            and user_credentials["password"] == "valid_password":
        return True
    return False


@pytest.mark.parametrize(
    "payload, expected_status_code",
    [
        [{"username": "existing_user", "password": "valid_password"}, 200],
        [{"username": "existing_user", "password": "wrong_password"}, 401],
    ]
)
@mock.patch("_6_mocking.app.main.check_user_credentials")
def test_check_credentials(mock_check_user_credentials, payload, expected_status_code):
    mock_check_user_credentials.side_effect = fake_check_credentials
    returned_status_code = login(payload)
    assert returned_status_code == expected_status_code


@pytest.mark.parametrize(
    "payload, expected_status_code",
    [
        [{"username": "existing_user", "password": "valid_password"}, 200],
        [{"username": "existing_user", "password": "wrong_password"}, 401],
    ]
)
def test_check_credentials_2(monkeypatch, payload, expected_status_code):
    monkeypatch.setattr(main_module, "check_user_credentials", fake_check_credentials)
    returned_status_code = login(payload)
    assert returned_status_code == expected_status_code


@mock.patch("_6_mocking.app.main.get_todo_from_rest")
def test_complete_todo(mocked_get_todo):
    mocked_get_todo.return_value = mock.Mock(name="request_response",
                                             **{"status_code": 200, "json.return_value": {"id": 1, 'completed': False}})
    assert complete_todo() == False
