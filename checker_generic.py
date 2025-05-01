"""Runner for assignment sanity checkers, including PyTA.
"""

import sys


def run_pyta(filename: str, config_file: str) -> None:
    """Run PYTA with configuration config_file on the file named filename.

    """

    sys.path.insert(0, 'pyta')
    import python_ta
    python_ta.check_all(filename, config=config_file)


def check(func: callable, args: list,
          expected: type) -> tuple[bool, object]:
    """Check if func(args) returns a result of type expected.

    Return (True, result-of-call) if the check succeeds.
    Return (False, error-or-failure-message) if anything goes wrong.
    """

    try:
        returned = func(*args)
    except Exception as exn:
        return (False, _error_message(func, args, exn))

    if isinstance(returned, expected):
        return (True, returned)

    return (False, _type_error_message(func, expected, returned))


def _type_error_message(func: callable, expected: type,
                        got: object) -> str:
    """Return an error message for function func returning got, where the
    correct return type is expected.

    """

    return (f'{func.__name__} should return a {expected.__name__},'
            f' but returned {got}')


def _error_message(func: callable, args: list,
                   error: Exception) -> str:
    """Return an error message: func(args) raised an error."""

    return (f"The call {func.__name__}({','.join(map(str, args))})"
            f' caused an error: {error}')
