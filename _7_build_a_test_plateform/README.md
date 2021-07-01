## Need for an automated solution

---

If we test a small system, running `pytest` should be enough to launch the test suite.
But if we need to deploy a more complex system, that should run in different environments, we might need to run pytests multiple time 
one for each env and isolate tests reports and coverage depending on which part of the system was under tests.

For that we need a CLI tool that could manage tests environment and is highly configurable.

## Tox to the rescue

Tox gives us the ability of running tests suits within different virtual environments that it creates based on a configuration file `tox.ini`
Tox needs at least a `setup.py` file OR a 
```ini
[tox]
envlist = webtest
```
Now that we define an environment (here called `webtest`), we can use its name in other configurations
The first thing we need to define is the environment itself under the tag `[testenv]`

```ini
[testenv]
# Define the interpreter for each enfironment
basepython =
    webtest: python3.8
# Define the dependencies (we can list each of them or just indicates the name of the requirements.txt file 
deps =
    webtest: -rrequirements-webtest.txt
# Define the commands to run for each environments (here we run the pytest command with the flag -m that allows us to select tests by markers
# Here only the test decorated by @pytest.mark.webtest will be run
commands =
    webtest: pytest -v -m "webtest"
```

Now we can run the `tox` command and it will run all the environments that we defined (Here we only define one which is `webtest` but if we had more than one, running the `tox` command will run them all).
Alternatively we can run only one environment by running the `tox <ENV_NAME>`. Here `tox webtest`. And only this environment will run.

