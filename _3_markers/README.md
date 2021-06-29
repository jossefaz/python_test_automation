## What "markers" are ?

---

As explained very well in the [docs](https://docs.pytest.org/en/6.2.x/mark.html#marking-test-functions-with-attributes), markers are simply decorators that help us to **set metadata** to our test.
This metadata will have an effect when running our test suits, and it could be fvery powerfull, helping us to organize tests by grouping them (for example), or injecting some pre-define parameters.

## Getting started 

---

Lets start with the simplest built-in marker provided by pytest which is the `skip` marker.

```python
import pytest
from ..app.main import add

# The following test will be skipped
@pytest.mark.skip
def test_add_num():
    assert add(1, 2) == 3

# The following test will run
def test_add_str():
    assert add("hello ", "world") == "hello world"

```

We can see the skipped test at the output :

```text
========== test session starts ===============================
platform linux -- Python 3.8.6, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /home/jossefaz/projects/python_test_automation
collected 2 items                                                                                                                                                                                                                                                                                                                                   

_3_markers/tests/test_main.py s.                                                                                                                                                                                                                                                                                                              [100%]

==================== 1 passed, 1 skipped in 0.01s ============
```

