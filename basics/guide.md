## Basic section : get started

---

Goal of this section is to getting familliar with testing basic concept and the pytest framwork (compared to the builtin unittest module)

We could forget it, but **testing** is actually one of the **foundation of computer science** : when we deal with binaries logic (AND/OR/XOR/XNOR...) and establish **truth table** for each of those statement, we are **preparing** tests by cover all possible cases.

## Definition

___

### Assertion
An assertion is a function that check if a given case is True. 
This function will **raise an exception** if a case is **False**.

### Unit Test
A Unit Test is made of 4 components.

1. **Arrange** : set of methods that helps to prepare the test (mocking, setUp, input data...)
2.  **Act** : function that will raise an exception. If it is not raising any exception, the test will be considered as passed (OK)
3. **Assert** : The statement that will raise the exception in the Act function (but any other exception that is raised )
4. **Cleanup** : set of method that will clean up what needed (open connections, test classes instance...)

During this session we will focus on **Act** and **Assert** only.






