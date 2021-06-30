## What and Why ?

--- 

In an Ideal world, every single function works like in bash : do one thing and do it very well. 

In such a world, test would be sugar, candy, very simple : just assert that the output is what I expect to be and that's it.

But most of the time it is not so simple. If a function has a dependency that will return a random result or takes times and is not mandatory for the behaviour under test...then we need something that will replace those dependencies by a predefined value.

This action is called mocking.

For example, if we want to test a `login` function, that will check credentials and return a status code.

```python
import requests

def check_user_credentials(user_credentials):
    return requests.post("https://mydomain/login", user_credentials)

def login(user_credentials):
    credentials = check_user_credentials(user_credentials)
    if not credentials:
        return 401
    return 200
```

We clearly have a problem here : `check_user_credentials` is an asynchronous code (that's not the problem !!) which return a result based on **real** users (send an HTTP Request to an authentication service and check there in the database if there is any user with the provided credentials).

Currently we just want to test the HTTP status code returned : 200 for correct credentials and 401 for incorrect ones.

3 main problem/challenges :

1. We don't want to provide a real user credentials in test (security purpose)
2. Since we provide a mock data, if we really check the credentials it will always (or 99%) fails
3. Even though it is not a real problem, we would like to avoid the communication latency between services for each test.

Solution : mocking the `check_user_credentials` function !

```python
from unittest import mock

import pytest
from ..app.main import login


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

```

`@mock.patch` takes as a parameter a import path ofthe targeted function to be macked. Under the hood it will replace all references inside the UUT by a [Mock object](https://docs.python.org/3/library/unittest.mock.html#the-mock-class).
The Mocke object has some attributes that allows us to control what this mocked function would return. 

By calling the `mocked_function.return_value` we make sure to get a constant result from this mocked function.

But here we also need to return a dynamic value based on the user credentials payload. 

So we use the `side_effect` attribute and we bind to it a function (here the `fake_check_credentials` that we defined before the test)

## The pytest way : MonkeyPatch

---

Pytest provide an easy way to mock. A built in fixture called [mockeypatch](https://docs.pytest.org/en/6.2.x/reference.html#monkeypatch).
We can easily call the mockeypatch inside the body of the test and perform a mock on the flight:

```python
import pytest
from ..app.main import login
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
def test_check_credentials_2(monkeypatch, payload, expected_status_code):
    monkeypatch.setattr(main_module, "check_user_credentials", fake_check_credentials)
    returned_status_code = login(payload)
    assert returned_status_code == expected_status_code

```


## The Mocking trap : making the test not testing anything !

---

In order to avoid this effect, we should apply two principles : 
1. Write the test BEFORE the code (ideally in a TDD way)
2. Define the behaviour under test : and DO NOT MOCK anything that is a part of this behaviour. 

In our example, the **request is NOT a part** of the behaviour (even if it looks like a part of it because it will define the return code). The behaviour under test is only the return statement of the login route.




