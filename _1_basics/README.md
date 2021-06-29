## Basic section : get started

---

Goal of this section is to getting familliar with testing basic concept and the pytest framwork (compared to the builtin unittest module)

We could forget it, but **testing** is actually one of the **foundation of computer science** : when we deal with binaries logic (AND/OR/XOR/XNOR...) and establish **truth table** for each of those statement, we are **preparing** tests by cover all possible cases.

## Definitions

___

### Assertion
An assertion is a function that check if a given case is True. 
This function will **raise an exception** if a case is **False**.

### SUT // UUT
System under test (SUT) or Unit Under Test (UUT) : defines a scope, a program or a part of it that acts like a state machine.
If not, it means that testing would be very hard. After all, testing test a *state*. 
If we look at function level, the state could be the input and the output. But at module level, the state could be a complex data structure that is being modified by different methods.
When we write a test, we should always ask ourselves before : 
1. what is my SUT
2. what is the state cases that I expect and what are those that I do NOT expect (state table)
3. Do I need any resource before testing my SUT
4. Do I need to clean up some resources that my test created (mock, files...etc)

### Test discovery

The way that a library or a framework (like pytest that we are using in the example), 

### Unit Test
When we look at the first time on a unit test, we could think of it as a simple function that will raise an exception. 
If it is not raising any exception, the test will be considered as passed (OK)

Even if it could be true. This statement is **largely incomplete**.


A Unit Test is made of 4 components.

1. **Arrange** : set of methods that helps to prepare the test (mocking, setUp, input data...)
2.  **Act** : Action that will change the state of the SUT, making the actual behavior. If it raises any **unhandled** exception, this will cause the test to fail.
3. **Assert** : The statement that will raise the exception in the Act function (but any other exception that is raised )
4. **Cleanup** : set of method that will clean up what needed (open connections, test classes instance...)

During this session we will focus on **Act** and **Assert** only.

## Practice

___

Let's define a simple function :

```python
# app/main.py
def add(a,b):
    return a+b
```

And now lets **assert** that the output is the expected one :

```python
# tests/test_main.py
from ..app.main import add

# Test discovery : the function name begins by "test_". This can be changed in the configuration file but this is the default configuration of pytest
def test_add_num():
    result = add(1,2) # <==== This is the Act (It will kick off a state change, here creating a result variable at the function scope
    assert result == 3 # <=== This is the assertion : We are checking if the state (or a part of it) is what we expect

def test_add_str():
    assert add("hello ", "world") == "hello world"
```

### Run the test

---

Run the command `pytest` from terminal (you might have to `pip install pytest` before if your terminal does not recognize the comman).

### Understanding the output 

---

There is 5 possible exit code for the `pytest` command :

**Exit code 0**
All tests were collected and passed successfully

**Exit code 1**
Tests were collected and run but some of the tests failed

**Exit code 2**
Test execution was interrupted by the user

**Exit code 3**
Internal error happened while executing tests

**Exit code 4**
pytest command line usage error

**Exit code 5**
No tests were collected

Each test will finnish by a letter in the `stdout`, here are the possibilities :

 - F - failed

- E - error

- s - skipped

- x - xfailed

- X - xpassed

- p - passed

- P - passed with output

For further flags of the `pytest` command [Read the docs !](https://docs.pytest.org/en/6.2.x/reference.html#command-line-flags)

Output example : we can see the `F` for "Failing" test and `E` for error on the traceback.

```text
collected 4 items                                                                                                                                                           

basics/tests/test_main.py ..F.                                                                                                                                        [100%]

================================================================================= FAILURES ==================================================================================
___________________________________________________________________________ TestMain.test_add_num ___________________________________________________________________________

self = <basics.tests.test_main.TestMain object at 0x7f23a0f4afd0>

    def test_add_num(self):
>       raise
E       RuntimeError: No active exception to reraise

basics/tests/test_main.py:11: RuntimeError
========================================================================== short test summary info ==========================================================================
FAILED basics/tests/test_main.py::TestMain::test_add_num - RuntimeError: No active exception to reraise
======================================================================== 1 failed, 3 passed in 0.06s ========================================================================


```


### Run Test classes

---
We can also define a class that includes a group of tests. This could be interesting for testing logic at class level **BUT** always keep in mind that 
for each method beginning by the discovery pattern ("test_" by default), pytest will create a new instance of the TestClass (by the way this is the discovery pattern for classes "Test")

```python
class TestMain:
    def test_add_num(self):
        assert add(1, 2) == 3

    def test_add_str(self):
        assert add("hello ", "world") == "hello world"
```

Output : 
```python
self = <basics.tests.test_main.TestMain object at 0x7f491fcba880>
self = <basics.tests.test_main.TestMain object at 0x7f491fcba9d0>
```

You notice that the TestMain instance have two different address, one for each method (test case), means that a new instance of the test class is created on each test case. 

So keep in mind if you use the instance selector - the self keyword at class level - ...it would be restored to initial state on each case in order to keep isolation from one test to another



## Exercise 

---

Create a test that will check if a given function will compute fibonacci nth number

## Bonus : Pycharm integrated pytest

---

By default, all test cases are discovered by Pycharm in the `unittest` fashion (i.e only if you write a class that inherits from the unittest.TestCase).
But there is a possibility to change this behaviour. Just go through : `Settings | Tools | Python Integrated tools | Testing` and change to your favorite framwork (pytest in our case)






