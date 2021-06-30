## Run the same test multiple times with different values ? Parameterize marker to the rescue 

---

Marker is not only a way to categorize or skip a test, it could be much powerful by providing us the capability of defining a special behavior to our test. 
When we will define our custom marker, we will see how powerful it could be. But there is also some built in markers that we could use in order to make our test suite more efficient.

One of them is the **parametrize** marker. It will allow us to run a test multiple times with different inputs.

## Practice 

---

Let's assume that we have a dummy login function that return a status code depending on the user login.

```python
def log_in(username: str, password: str) -> int:
    if username == "john" and password == "supersecret":
        return 200
    # Return 401 unauthorized
    return 401
```

For sure, we could make two tests : on to test valid credentials that return 200 and another one that test the unauthorize user that return 401 HTTP status code.

But we also could save time and lines of code by runing the same test multiple times with different expected output.

This is where the marker parametrize comes in 

```python
@pytest.mark.parametrize("username, password, expected_status_code",
                          [("john", "supersecret", 200),
                           ("john", "wrongpassword", 401),
                           ("wronguser", "supersecret", 401)])
def test_login(username, password, expected_status_code):
    assert log_in(username,password) == expected_status_code
```

We first define a string with name of each parameter separated by comma, then we open an array