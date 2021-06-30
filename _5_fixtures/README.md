## What is a fixture ?

---

A test fixture is a component that could be used to define a test environment. When Apple or Samsung realease a new smartphone, 
they will test it in many ways. On of them is a temperature machine where the smartphones are put into and very high (or low) temperature is raised in order to check the robustness of the product.
This machine is actually a test fixture.

In the software field, a text fixture could be every kind of tool (db connections, cache object, draft folder...) that we need for our test suite in order to get the expected behaviour.
If a function needs to save a file in a directory, then, instead of creating this directory inside the test function, a fixture that will create and remove this temporary folder could be a great solution.

## Pytest way : dependency injection 

---

If you come from JAVA or other static typed OOP language, then you are probably familiar with the DI design pattern.
It is based on establishing contract through interfaces and allow a very high modularity when instantiating objects.

In python, which is dynamic typed language, the concept of interface does not exists. But, we can allow a kind of DI by looking up the parameters name of a given function.
We can build a registry that holds the name of a parameter as a key and a reference to a class or to a function as a value.

Then, if one of the function called within a specific context (that handle and inspect parameters name) has a match in our registry, we will replace that paras by the reference of the function it has in value.

Fixtures in pytest works the same way. Whenever a test function is executed, Pytest will scan the parameters names and will check if one of them are actually a presents in its fixtures registry. If yes, it will call this function and inject the result of it to the test function

## Practice

---

Lets define a very simple function that need a database connection :

```python
def retrieve_users(db_connection) :
    if db_connection.connected :
        return "All users"
    return "Not Connected to db"
```

In order to test this function we will create a fake db class :

```python
class DummyDb:
    def __init__(self):
        self.connected = False

    def connect(self):
        self.connected = True
```

Then, instead of instantiate this `DummyDB` inside the test, we will create a fixture for it, using the fixture decorator :

```python
@pytest.fixture
def db_connection():
    conn = DummyDb()
    conn.connect()
    return conn
```
Then pass the exact same name as a positional argument to the test function 

```python
from ..app.main import retrieve_users
# Notice the name of the parameter which is the exact same name of the fixture that we defined before
def test_retrieve_users(db_connection):
    assert retrieve_users(db_connection) == "All users"
```

## Built in fixture