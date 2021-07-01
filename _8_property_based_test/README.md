## The problem : static data won't reach Edge Case

---

When we run unit test, we could very fast fall in the trap of mocking everything and basically not testing the behaviour that we attempt to test.
Another famous trap is to give to our UUT a very specific data as an input on which we know that the test will pass

```python
from dataclasses import dataclass
class Person:
    age:int
    name:str

def check_person_age(person:Person):
    if person.age < 18 : 
        print("You are under 18")
    print("You can vote, you are an adult")
```

Let's write our test :

```python
# We use the capsys built in fixture from pytest in order to test the prints statements
def test_check_person_age_under_18(capsys):
    check_person_age(Person(15, "John"))
    assert capsys.readouterr().out.strip() == "You are under 18"

# We use the capsys built in fixture from pytest in order to test the prints statements
def test_check_person_age_over_18(capsys):
    check_person_age(Person(19, "John"))
    assert capsys.readouterr().out.strip() == "You can vote, you are an adult"
```

This is really comfortable because we define the age here. But we need to write two tests for that.
Let's try what hypotesis can do for us 

```python
from hypothesis import given, strategies as st

@given(p=st.builds(Person))
def test_check_person_age(capsys, p):
    check_person_age(p)
    if p.age > 18 :
        assert capsys.readouterr().out.strip() == "You can vote, you are an adult"
    else :
        assert capsys.readouterr().out.strip() == "You are under 18"
```

Based on a Dataclass, Hypotesis render at each run a new person.