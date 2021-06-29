import pytest

from ..app.main import add

#
# # The following test will be skipped
# @pytest.mark.skip
# def test_add_num():
#     assert add(1, 2) == 3
#
#
# # The following test will be skipped with a given reason on stdout
# @pytest.mark.skip(reason="This test should not be run at any case")
# def test_add_num_2():
#     assert add(1, 2) == 3
#
#
# SEM_VER = "2.0.0"
#
#
# # The following test will be skipped if the first argument provided to the skipif marker is True
# @pytest.mark.skipif(SEM_VER != "1.0.0", reason="This test is only valid for the version 1.0.0")
# def test_add_num_3():
#     assert add(1, 2) == 3

@pytest.mark.xfail(reason="Under construction ...")
def test_add_str_2():
    raise


# def test_add_str():
#     assert add("hello ", "world") == "hello world"
