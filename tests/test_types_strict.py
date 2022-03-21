from typing import Any, Callable, Optional
import pytest
from datastructures.types import strict


@strict
def t_no_annotations(a):
    print(a)
    return True


@strict
def t_no_annotations_optional(a, b, c=None):
    print(a)
    print(b)

    if c:
        print(c)

    return True


@strict
def t_partial_annotations(a, b: bool):
    if b:
        print(a)

    return True


@strict
def t_partial_annotations_optional(a, b: bool, c=None):
    if b:
        print(a)

    if c:
        print(c)

    return True


@strict
def t_partial_annotations_optional_annotated(a, b: bool, c: bool = False):
    if b:
        print(a)

    print(c)

    return True


@strict
def t_annotations(a: int):
    print(a)

    return True


@strict
def t_annotations_optional(a: int, b: bool = False):
    print(a)
    print(b)
    return True


@strict
def t_any(a: Any, b):
    print(a)
    print(b)
    return True


@strict
def t_optional_any(a: Any, b: Any = None):
    print(a)
    print(b)
    return True


@strict
def t_callable(a: Callable, b):
    print(a)
    print(b)
    return True


@strict
def t_optional_callable(a: Any, b: Optional[Callable] = None):
    print(a)
    print(b)
    return True


def f():
    return True


l = lambda: True
l_args = lambda x: x

### Tests ###


def test_no_annotations():

    assert t_no_annotations("a")
    assert t_no_annotations(1)
    assert t_no_annotations(False)
    assert t_no_annotations(f)


def test_no_annotations_optional():
    assert t_no_annotations_optional("a", 2)
    assert t_no_annotations_optional(1, 5, False)
    assert t_no_annotations_optional(False, "a", c="c")


@pytest.mark.skip(
    reason=
    "The current implementation does not work well with skipping arguments. Fixing that soon."
)
def test_partial_annotations():
    # TODO rewrite to use funciton signatures
    assert t_partial_annotations(1, True)
    assert t_partial_annotations(1, False)
    assert t_partial_annotations("c", False)
    assert t_partial_annotations(True, False)

    with pytest.raises(TypeError):
        t_partial_annotations(True, "a")

    with pytest.raises(TypeError):
        t_partial_annotations(1, 1)


@pytest.mark.skip(
    reason=
    "The current implementation does not work well with skipping arguments. Fixing that soon."
)
def test_partial_annotations_optional():
    assert t_partial_annotations_optional(1, True, 1)
    assert t_partial_annotations_optional(1, False, 1)
    assert t_partial_annotations_optional(1, False)
    assert t_partial_annotations_optional(1, True)
    assert t_partial_annotations_optional(1, False, c="abc")
    assert t_partial_annotations_optional(1, True, c=8)

    with pytest.raises(TypeError):
        t_partial_annotations_optional(1, "abc", 1)

    with pytest.raises(TypeError):
        t_partial_annotations_optional(1, 1, 1)

    with pytest.raises(TypeError):
        t_partial_annotations_optional(1, "abc")

    with pytest.raises(TypeError):
        t_partial_annotations_optional(1, 1)

    with pytest.raises(TypeError):
        t_partial_annotations_optional(1, "abc", c="abc")

    with pytest.raises(TypeError):
        t_partial_annotations_optional(1, 8, c=8)


@pytest.mark.skip(
    reason=
    "The current implementation does not work well with skipping arguments. Fixing that soon."
)
def test_partial_annotations_optional_annotated():
    assert t_partial_annotations_optional_annotated(1, False)
    assert t_partial_annotations_optional_annotated(1, True)
    assert t_partial_annotations_optional_annotated(1, False, True)
    assert t_partial_annotations_optional_annotated(1, True, False)
    assert t_partial_annotations_optional_annotated(1, False, c=True)
    assert t_partial_annotations_optional_annotated(1, True, c=False)

    with pytest.raises(TypeError):
        t_partial_annotations_optional_annotated(1, False, c="abc")

    with pytest.raises(TypeError):
        t_partial_annotations_optional_annotated(1, True, c=8)

    with pytest.raises(TypeError):
        t_partial_annotations_optional_annotated(1, False, 1)

    with pytest.raises(TypeError):
        t_partial_annotations_optional_annotated(1, True, 1)

    with pytest.raises(TypeError):
        t_partial_annotations_optional_annotated(1, "abc", 1)

    with pytest.raises(TypeError):
        t_partial_annotations_optional_annotated(1, 1, 1)

    with pytest.raises(TypeError):
        t_partial_annotations_optional_annotated(1, "abc")

    with pytest.raises(TypeError):
        t_partial_annotations_optional_annotated(1, 1)

    with pytest.raises(TypeError):
        t_partial_annotations_optional_annotated(1, "abc", c="abc")

    with pytest.raises(TypeError):
        t_partial_annotations_optional_annotated(1, 8, c=8)


def test_annotations():
    assert t_annotations(1)

    with pytest.raises(TypeError):
        t_annotations("abc")

    with pytest.raises(TypeError):
        t_annotations(True)


def test_annotations_optional():
    assert t_annotations_optional(1)
    assert t_annotations_optional(1, True)
    assert t_annotations_optional(1, b=False)

    with pytest.raises(TypeError):
        t_annotations_optional(True)

    with pytest.raises(TypeError):
        t_annotations_optional("abc")

    with pytest.raises(TypeError):
        t_annotations_optional(1, 1)

    with pytest.raises(TypeError):
        t_annotations_optional(True, 1)

    with pytest.raises(TypeError):
        t_annotations_optional(1, b=1)

    with pytest.raises(TypeError):
        t_annotations_optional(True, b=1)


@pytest.mark.xfail
def test_any():
    # TODO Any is weird, because the types don't match,
    #      but it should still work.
    assert t_any(f, f)
    assert t_any(1, f)
    assert t_any(True, 1)
    assert t_any("", "abc")


@pytest.mark.xfail
def test_optional_any():
    # TODO Any is weird, because the types don't match,
    #      but it should still work.
    assert t_optional_any(f, f)
    assert t_optional_any(1, f)
    assert t_optional_any(True, 1)
    assert t_optional_any("", "abc")

    assert t_optional_any(f)
    assert t_optional_any(1)
    assert t_optional_any(True)
    assert t_optional_any("")


@pytest.mark.xfail
def test_callable():
    # TODO this does not work because function != callable
    assert t_callable(f, f)
    assert t_callable(l, l)
    assert t_callable(f, 1)
    assert t_callable(l, True)
    assert t_callable(l_args, True)
    assert t_callable(l_args, 1)
    assert t_callable(l, l_args)
    assert t_callable(l_args, l)

    with pytest.raises(TypeError):
        t_callable(1, f)

    with pytest.raises(TypeError):
        t_callable(True, 1)

    with pytest.raises(TypeError):
        t_callable(1, 1)

    with pytest.raises(TypeError):
        t_callable(True, True)

    with pytest.raises(TypeError):
        t_callable(True, l_args)

    with pytest.raises(TypeError):
        t_callable(1, l_args)

    with pytest.raises(TypeError):
        t_callable("abc", l)


@pytest.mark.xfail
def test_optional_callable():
    # TODO this does not work because of Any
    assert t_optional_callable(f, f)
    assert t_optional_callable(l, b=l)
    assert t_optional_callable(1, l)
    assert t_optional_callable(True, f)
    assert t_optional_callable(True, b=l_args)
    assert t_optional_callable("abc", b=f)

    assert t_optional_callable(f)
    assert t_optional_callable(l)
    assert t_optional_callable(1)
    assert t_optional_callable(True)
    assert t_optional_callable(True)
    assert t_optional_callable("abc")

    with pytest.raises(TypeError):
        t_optional_callable(l, 1)

    with pytest.raises(TypeError):
        t_optional_callable(True, 1)

    with pytest.raises(TypeError):
        t_optional_callable(1, 1)

    with pytest.raises(TypeError):
        t_optional_callable(True, True)

    with pytest.raises(TypeError):
        t_optional_callable(l_args, True)

    with pytest.raises(TypeError):
        t_optional_callable(l_args, 1)

    with pytest.raises(TypeError):
        t_optional_callable("abc", "abc")
