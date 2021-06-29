## Basic section : get started

---

Goal of this section is to getting familliar with testing basic concept and the pytest framwork (compared to the builtin unittest module)

We could forget it, but **testing** is actually one of the **foundation of computer science** : when we deal with binaries logic (AND/OR/XOR/XNOR...) and establish **truth table** for each of those statement, we are **preparing** tests by cover all possible cases.

## Definitions

___

### Assertion
An assertion is a function that check if a given case is True. 
This function will **raise an exception** if a case is **False**.

### SUT 
System under test (SUT) : defines a scope, a program or a part of it that acts like a state machine.
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

## Exercise 

---

Create a test that will check if a given function will raise a ValueError in case of negative integer input.








