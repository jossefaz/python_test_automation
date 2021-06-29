import pytest

from ..app.main import enter_the_pub


def test_cannot_enter_the_pub():
    with pytest.raises(ValueError) as exc_info:
        enter_the_pub(15)
    assert str(exc_info.value) == "Consuming Alcohol is not permitted under 18 years old"