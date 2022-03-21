def strict(func):
    """
    Decorator to enforce typehints.

    :raises: :class:`TypeError` if the annotated types don't match the input types
    """

    def wrap(*args, **kwargs):
        annotations = func.__annotations__

        for arg, var in zip(args, annotations):
            if type(arg) is not annotations[var]:
                raise TypeError(
                    f"Annotated type {annotations[var]} does not match the input type {type(arg)}"
                )

        for oarg in kwargs:
            if oarg in annotations.keys() and type(
                    kwargs[oarg]) is not annotations[oarg]:
                raise TypeError(
                    f"Annotated type {annotations[oarg]} does not match the input type {type(kwargs[oarg])}"
                )

        return func(*args, **kwargs)

    return wrap
