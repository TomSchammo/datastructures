from typing import Any, Callable, Generic, Optional, TypeVar
from inspect import getcallargs

from datastructures.exceptions import NoException

V = TypeVar("V")
E = TypeVar("E", bound=BaseException, covariant=True)


class Result(Generic[V, E]):
    """
    Result is a data structure that can be used to call a function that might fail.
    The error is catched and stored in the :class:`Result` on a failure.
    On a success the value is stored and can be accessed via different class methods.

    Keep in mind that any Exception will be catched.
    """

    __value: V
    __error: E

    def __init__(self, func: Callable, *args, **kwargs) -> None:
        """
        :param func:      The function to run
        :param *args:     The arguments of func
        :param **kwargs:  The positional arguments of func

        :raises: :class:`TypeError` if the user did not provide the correct arguments.
        """

        # NOTE: Making sure that the user has actually provided
        #       the required function arguments.
        getcallargs(func, *args, **kwargs)

        try:
            self.__value = func(*args, **kwargs) if args else func()
            self.__error = NoException()

        except BaseException as e:
            self.__value = None
            self.__error = e

    def get(self) -> Optional[V]:
        """
        Retrieves the value of the object if the exception
        is of type :class:`NoException` (so there is no exception).

        :return: The value stored in the result or None
        """

        if self._get_error_type() is NoException:
            return self.__value

        else:
            return None

    def get_or(self, alt: V) -> V:
        """
        Retrieves the value of the object if the exception
        is of type :class:`NoException` (so there is no exception).

        If there is, the alternative value provided will be returned instead.

        :param alt: The alternative value in case of an error.

        :return: The value stored in the result or alt

        :raises: :class:`TypeError` if the type of `alt` is not the
                 same as the return value of the executed function.
        """

        if type(alt) is not type(self.__value):
            raise TypeError

        if type(self.__error) is NoException:
            assert self.__value is not None
            return self.__value

        else:
            return alt

    def get_or_any(self, alt: V) -> Any:
        """
        Retrieves the value of the object if the exception
        is of type :class:`NoException` (so there is no exception).

        If there is, the alternative value provided will be returned instead.

        :param alt: The alternative value in case of an error.

        :return: The value stored in the result or alt
        """

        if type(self.__error) is NoException:
            return self.__value

        else:
            return alt

    def raise_error(self):
        """
        Raises the Exception in Result.

        The type of this Exception for exception handling purposes
        can be retrieved using the internal '_get_error_type' function.

        :raises: :class:`E`

        :raises: :class:`TypeError` If the type of the error cannot be raised.
                           This should never happen, but is kept as an
                           additional sanity check.
        """

        if isinstance(self.__error, BaseException):
            raise self.__error
        else:
            raise TypeError(f"Cannot raise type '{self._get_error_type()}'")

    def _get_error_type(self):
        """
        Returns the type of the stored exception.

        :return: Type of self.__error
        """

        return type(self.__error)
