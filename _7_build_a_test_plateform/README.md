## Need for an automated solution

---

If we test a small system, running `pytest` should be enough to launch the test suite.
But if we need to deploy a more complex system, that should run in different environments, we might need to run pytests multiple time 
one for each env and isolate tests reports and coverage depending on which part of the system was under tests.

For that we need a CLI tool that could manage tests environment and is highly configurable.

## Tox to the rescue

