import pytest
from datastructures.result import Result, NoException


def t_return():
    return 1


def t_multiple_args(b1: bool, b2: bool):
    return b1 and b2


def t_optional_args(b1: bool, b2: bool = True):
    return b1 and b2


def t_raise():
    raise BaseException


def t_raise_return(b1: bool, b2: bool) -> int:
    if b1 and b2:
        raise NotImplementedError
    else:
        return 1


def t_raise_return_optional(b1: bool, b2: bool = True):
    if b1 and b2:
        raise KeyboardInterrupt
    elif b1 or b2:
        return 5
    else:
        return 1


def test_no_args():

    result = Result(t_return)

    assert result._Result__value == 1
    type(result._Result__error) == NoException


def test_args():

    result = Result(t_multiple_args, True, True)

    assert result._Result__value == True
    assert type(result._Result__error) == NoException


def test_optional_args():

    result = Result(t_optional_args, True)

    assert result._Result__value == True
    assert type(result._Result__error) == NoException


def test_raise_no_args():

    result = Result(t_raise)

    assert result._Result__value == None
    assert type(result._Result__error) == BaseException


def test_raise_args():

    result = Result(t_raise_return, True, True)

    assert result._Result__value == None
    assert type(result._Result__error) == NotImplementedError

    result2 = Result(t_raise_return, True, False)

    assert result2._Result__value == 1
    assert type(result2._Result__error) == NoException


def test_raise_optional_args():

    result = Result(t_raise_return_optional, True)

    assert result._Result__value == None
    assert type(result._Result__error) == KeyboardInterrupt

    result2 = Result(t_raise_return_optional, False)

    assert result2._Result__value == 5
    assert type(result2._Result__error) == NoException

    result3 = Result(t_raise_return_optional, False, b2=False)

    assert result3._Result__value == 1
    assert type(result3._Result__error) == NoException


def test_wrong_args():

    with pytest.raises(TypeError):
        _ = Result(t_return, b2=False)

    with pytest.raises(TypeError):
        _ = Result(t_multiple_args)

    with pytest.raises(TypeError):
        _ = Result(t_multiple_args, False)

    with pytest.raises(TypeError):
        _ = Result(t_raise_return, False)


def test_methods_no_args():

    result = Result(t_return)

    assert result.get() == 1
    assert result._get_error_type() == NoException

    with pytest.raises(NoException):
        result.raise_error()


def test_methods_args():

    result = Result(t_multiple_args, True, True)

    assert result.get() == True
    assert result._get_error_type() == NoException

    with pytest.raises(NoException):
        result.raise_error()


def test_methods_optional_args():

    result = Result(t_optional_args, True)

    assert result.get() == True
    assert result.get_or(False) == True
    assert result._get_error_type() == NoException

    with pytest.raises(NoException):
        result.raise_error()


def test_methods_raise_no_args():

    result = Result(t_raise_return, True, True)

    assert result.get() == None
    assert result.get_or(0) == 0
    assert result._get_error_type() == NotImplementedError

    with pytest.raises(NotImplementedError):
        result.raise_error()


def test_methods_raise_args():

    result = Result(t_raise_return, True, True)

    assert result.get() == None
    assert result.get_or(0) == 0
    assert result._get_error_type() == NotImplementedError

    with pytest.raises(NotImplementedError):
        result.raise_error()

    result2 = Result(t_raise_return, True, False)

    assert result2.get() == 1
    assert result2.get_or(0) == 1
    assert result2._get_error_type() == NoException

    with pytest.raises(NoException):
        result2.raise_error()


def test_methods_raise_optional_args():

    result = Result(t_raise_return_optional, True)

    assert result.get() == None
    assert result.get_or(0) == 0
    assert result.get_or("abc") == "abc"
    assert result.get_or_any("abc") == "abc"
    assert result.get_or_any(0) == 0
    assert result._get_error_type() == KeyboardInterrupt

    with pytest.raises(KeyboardInterrupt):
        result.raise_error()

    result2 = Result(t_raise_return_optional, False)

    assert result2.get() == 5
    assert result2.get_or(0) == 5
    assert result2.get_or_any("abc") == 5
    assert result2._get_error_type() == NoException

    with pytest.raises(NoException):
        result2.raise_error()

    result3 = Result(t_raise_return_optional, False, b2=False)

    assert result3.get() == 1
    assert result3.get_or(0) == 1
    assert result3.get_or_any("abc") == 1
    assert result3._get_error_type() == NoException

    with pytest.raises(NoException):
        result3.raise_error()


def test_typehints():

    result = Result[int, BaseException](t_raise)

    assert result.get() == None
    assert result.get_or(0) == 0

    with pytest.raises(TypeError):
        result.get_or("abc")

    assert result.get_or_any("abc") == "abc"
