import pytest

from ..app.main import check_person_age, Person
from hypothesis import example, given, settings, strategies as st
from hypothesis import HealthCheck


# We use the capsys built in fixture from pytest in order to test the prints statements
def test_check_person_age(capsys):
    check_person_age(Person(15, "John"))
    assert capsys.readouterr().out.strip() == "You are under 18"


@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(p=st.builds(Person))
def test_check_person_age(capsys, p):
    check_person_age(p)
    if p.age > 18 :
        assert capsys.readouterr().out.strip() == "You can vote, you are an adult"
    else :
        assert capsys.readouterr().out.strip() == "You are under 18"

