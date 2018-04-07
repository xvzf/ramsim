from . import RunnerException


def assert_true(pline: int, value: bool, msg=None):
    if not value:
        if not msg:
            raise RunnerException(f"Runtime Error on line {pline}, check your code")
        else:
            raise RunnerException(f"Runtime Error in Line{pline}, {msg}")