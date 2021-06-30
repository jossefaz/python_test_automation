## What is a fixture ?

---

A test fixture is a component that could be used to define a test environment. When Apple or Samsung realease a new smartphone, 
they will test it in many ways. On of them is a temperature machine where the smartphones are put into and very high (or low) temperature is raised in order to check the robustness of the product.
This machine is actually a test fixture.

In the software field, a text fixture could be every kind of tool (db connections, cache object, draft folder...) that we need for our test suite in order to get the expected behaviour.
If a function needs to save a file in a directory, then, instead of creating this directory inside the test function, a fixture that will create and remove this temporary folder could be a great solution.

So if we recall the 4 steps of a test (from the **basics** section), we now understand that fixture is actually relevant for the **Arrange** and **Cleanup** steps (it kind of "replace" the ***setUp*** and ***tearDown*** methods from the ***unittest*** module)

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

---

Pytest comes with a set of very useful [built-in fixtures](https://docs.pytest.org/en/6.2.x/builtin.html#pytest-api-and-builtin-fixtures) . 
Lets have a look on the `tmpdir` fixture

Lets define a simple function that write input text in a file :

```python
def save_text_in_file(text: str, file_path: str):
    with open(file_path, "w+") as fp:
            fp.write(text)
```
We can use the `tmpdir` fixture here as a draft directory :


```python
import os
from ..app.main import save_text_in_file

#Here tmpdi is a name of a builtin fixture and will be replaced by pytest automaticaly by the path of a temp directory
def test_write_text_to_file(tmpdir):
    file_name = "dummy_file.txt"
    file_path = os.path.join(tmpdir, file_name)
    text_to_write = "Hello World"
    
    save_text_in_file(text_to_write, file_path)
    with open(file_path, 'r') as fp:
        assert fp.readline() == text_to_write
```

## Conftest.py : Where all fixtrues should be defined

--- 

According to the [docs](https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files), Pytest will lookup for fixtures in a single file called `conftest.py`.
Even though you can define and use `@pytest.fixture` in every part of the code, the best way to share fixtures among all the test code base is to write them all in the `conftest.py` file.


## Exercise : Create a fixture factory

---

Since a fixture is a simple function, we can return another function from it which could be a factory that will generate random data for us.

In this exercise, our Domain will be Mutants (like X-MEN). 
A mutant has 3 properties :
1.  **power** (Could be one of :Ice, Fire, Psycho, Self_recovery)
2. **strength** (Could be one of :Weak,Middle,Strong,God)
3. **family** (Could be one of :Beast,Mind,Daemons,Angels")

We have this function : 
```python
def fight_mutants(army_of_mutants: List[Mutant]):
    return max(army_of_mutants, key=lambda m: m.strength)
```
Write a test (and other stuff also like the Mutant class), that will generate a great X-Men army (given the nth number of mutants) and will test the `fight_mutants` function (asserting that the last survivor is indeed a mutant by checking its properties)
This test should be run with a fixture that will generate the army for you (a different army at each test running).


## Bonus : Parametrize a fixture using the indirect and request objects

---

If you did the exercise thaen you probably return a function from a fixture. How can we run this returned function with differents parameters from the paramtrize mark ?
When using the `@pytest.mark.parametrize` we can add an `indirect` attribute to it, meaning that the exact parameter is actually an argument to pass to a fixture

```python

@pytest.mark.paramtrize("my_fixture, another_param", [
    ('argument_for_the_fixture', 'another_argument_passed_to_the_function'),
    ('argument_for_the_fixture2', 'another_argument_passed_to_the_function2')
], indirect=["my_fixture"])
def test_fixture_param(my_fixture, another_param):
    # the my_fixture will actually contains the fixture output with the argument provided in the params array (here 'argument_for_the_fixture' and 'argument_for_the_fixture2' at the second run) 
    a_fixture_return = my_fixture
    
```

