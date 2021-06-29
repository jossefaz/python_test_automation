## Goals : How to assert an exception

---

### The Problem

If you recall from the last session (where we define what an assertion is), then you would probably ask yourself : 

if an assertion is a function that will raise an exception, 

And a test is considered as **"Fail"** on every exception that could occurs both on the **Act** and **Assertion** steps (please refere to the `basics` for those two terms)

then how can we test an exception that occurs explicitly in the **Act** ? 

For example if I want to try that an input is negative and I want to raise a ValueError if not :

```python
def enter_the_pub(age:int) -> None :
    if (age < 18) :
        raise ValueError("Consuming Alcohol is not permitted under 18 years old")
    # Continue processing
```

If we test a case with an age under 18 that test will fail ! We want a test that check the behaviour of `enter_the_pub`. And if `enter_the_pub` raise an exception because the input is under 18, then it is the expected behaviour and I want my test to pass on that specific behavior.

### The Pytest Solution : context manager

For that particular case, pytest provides us a context manager. All **acts** within this context should raise the exact same exception provided as an argument to the context manager :

```python
import pytest

def test_cannot_enter_the_pub():
    with pytest.raises(ValueError):
        enter_the_pub(15)

```

Here the `raises` method of pytest has an `__exit__` implementation that check on every execution within this context that it raises the expected exception :

### Deep dive

Lets have a look on the source code (especially look at the `__exit__` function) :

```python
# _pytest/python_api.py
class RaisesContext(Generic[_E]):
    def __init__(
        self,
        expected_exception: Union[Type[_E], Tuple[Type[_E], ...]],
        message: str,
        match_expr: Optional[Union[str, Pattern[str]]] = None,
    ) -> None:
        self.expected_exception = expected_exception
        self.message = message
        self.match_expr = match_expr
        self.excinfo: Optional[_pytest._code.ExceptionInfo[_E]] = None

    def __enter__(self) -> _pytest._code.ExceptionInfo[_E]:
        self.excinfo = _pytest._code.ExceptionInfo.for_later()
        return self.excinfo #<=== Return an execution information object !

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        __tracebackhide__ = True
        if exc_type is None:
            fail(self.message) 
        assert self.excinfo is not None # <=== if there is no exception after the context execution it fails
        if not issubclass(exc_type, self.expected_exception):
            return False # <=== if the raised exception is not the expected exception it will fail too !
        # Cast to narrow the exception type now that it's verified.
        exc_info = cast(Tuple[Type[_E], _E, TracebackType], (exc_type, exc_val, exc_tb))
        self.excinfo.fill_unfilled(exc_info)
        if self.match_expr is not None:
            self.excinfo.match(self.match_expr) #<=== Check the match message error
        return True

```

### Handle more than the exception type

Sometimes we want to check further and not only the type of the exception.
We saw in the **Deep dive** that the return type of the `__enter__` method is an `excinfo` object. This object has some properties that we can use for example to check the error message that our function return :

```python
import pytest

def test_cannot_enter_the_pub():
    with pytest.raises(ValueError) as exc_info:
        enter_the_pub(15)
    # call the __str__ function of the exception object and assert its value
    assert str(exc_info.value) == "Consuming Alcohol is not permitted under 18 years old"

```

But actually if we take a look at the `__init__` signature of `RaisesContext` class, we notice the `match_expression` (which come from the `match` parameter of `pytest.raises`), this is a message that we can provid as the expected message from the exception

```python
import pytest

def test_cannot_enter_the_pub():
    
    with pytest.raises(ValueError, match="Consuming Alcohol is not permitted under 18 years old") as exc_info:
        enter_the_pub(15)

```

### Exercise

---

Write a test that will check for a missing argument and output a custom message for number of positional missing argument and keyword missing arguments