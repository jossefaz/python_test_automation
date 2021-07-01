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


## More on Mock

---

The mock API of the `unittest` module has a lot of feature that could be use for example to mock nested function call and return values.
Let's say that we need to mock a  REST API calling using the `requests` library. But our UUT needs to get back a Response object (Which can call the `json()` method on and return a valid json).

```python
import requests
from requests import Response

def get_todo_from_rest():
    response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
    return response
#Return {'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': False}

def is_todo_completed(todo:Response):
    parsed_todo = todo.json()
    return parsed_todo["completed"]

def complete_todo():
    todo = get_todo_from_rest()
    if is_todo_completed(todo) : 
        return True
    return False    

```
We want to test the `complete_todo` method. For that we need to mock the  `get_todo_from_rest` to avoid the API call and to ensure that we will get back an object with a callable `json()` method.

```python
from unittest import mock
from ..app.main import complete_todo

# We first patch the get_todo_from_rest 
@mock.patch("_6_mocking.app.main.get_todo_from_rest")
def test_complete_todo(mocked_get_todo):
    # We use the Mock class to mock a response (a mock object could be used both as a function or to return a value)
    # From the docs : Mocks can also be called with arbitrary keyword arguments. These will be used to set attributes on the mock after it is created. See the configure_mock() method for details.
    # We use this ability by calling a dictionnary and immediatly destructure it (we could call status_code=200 but here we need the json to be a mock too. And since we cannot use '.' as a kwarg we use a dictionnary here
    mocked_get_todo.return_value = mock.Mock(name="request_response",
                                             **{"status_code": 200, "json.return_value": {"id": 1, 'completed': False}})
    assert complete_todo() == False
```
The advantage of using the `moc.Mock` class from the `unittest` module over the `monkeypatch` fixture, is the access to a bunch of useful method to assert that the **patched** function was called a number of time.
For example :

```python

from unittest import mock
from ..app.main import complete_todo

# We first patch the get_todo_from_rest 
@mock.patch("_6_mocking.app.main.get_todo_from_rest")
def test_complete_todo_called_once(mocked_get_todo):
    mocked_get_todo.return_value = mock.Mock(name="request_response",
                                             **{"status_code": 200, "json.return_value": {"id": 1, 'completed': False}})
    complete_todo()
    mocked_get_todo.assert_called_once()
```

All the `assert_called` method could be found [HERE](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.assert_called)

## Mock side_effect method






