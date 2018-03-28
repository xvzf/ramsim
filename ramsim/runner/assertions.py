from . import RunnerException


def assert_true(pline: int ,value: bool):
    if not value:
        raise RunnerException(f"Runtime Error on line {pline}, check your code")