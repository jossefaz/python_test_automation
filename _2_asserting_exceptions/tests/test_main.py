import pytest

from ..app.main import enter_the_pub


def test_cannot_enter_the_pub():
    with pytest.raises(ValueError):
        enter_the_pub(15)