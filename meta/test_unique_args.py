import pytest

from unique_args import UniqueArgs


class BaseClass(metaclass=UniqueArgs):
    def __init__(self, base_init_arg):
        ...

    def foo(self, foo_arg):
        ...


def test_unique_args():
    b = type('B', (BaseClass,), {'bar': lambda b_arg: ...})


def test_duplicated_arg():
    with pytest.raises(ValueError):
        type('B', (BaseClass,), {'bar': lambda base_init_arg: ...})


def test_duplicate_arg_lower_in_mro():
    b = type('B', (BaseClass,), {'bar': lambda b_arg: ...})
    with pytest.raises(ValueError):
        type('C', (b,), {'baz': lambda b_arg, foo_arg: ...})


def test_overloaded_method_with_different_signature():
    with pytest.raises(ValueError):
        type('B', (BaseClass,), {'foo': lambda base_init_arg: ...})


# def test_duplicate_arg_in_inheritance_side_branch():
#     br1 = type('Br1', (BaseClass,), {'bar': lambda b1_arg: ...})
#     br1_a = type('Br1_A', (br1,), {})
#     br1_b = type('Br1_B', (br1_a,), {'baz': lambda b1_b_arg: ...})
#
#     br2 = type('Br2', (BaseClass,), {'bar': lambda b2_arg: ...})
#     br2_a = type('Br2_A', (br2,), {})
#     br2_b = type('Br2_B', (br2_a,), {'baz': lambda b1_a_arg: ...})  # TODO: should raise
