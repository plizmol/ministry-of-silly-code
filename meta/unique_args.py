from typing import Iterable
from inspect import signature


class UniqueArgs(type):
    """
    Metaclass that force you to make all argument names unique across class hierarchy.
    Ignores self and cls and all dunder methods except __init__
    """
    def __new__(cls, name, bases, namespace):
        class_obj = super().__new__(cls, name, bases, namespace)
        seen = set()
        for ancestor in class_obj.__mro__[1:-1]:  # 1 is the class_obj itself, -1 is type
            seen.update(cls._get_args_set(ancestor, dir(ancestor)))

        new_args = cls._get_args_set(class_obj, namespace)
        non_unique = seen.intersection((new_args - {'self', 'cls'}))
        if non_unique:
            raise ValueError(f'{non_unique} args violate uniqueness constraint')
        return class_obj

    @staticmethod
    def _get_args_set(cls_obj, iterable: Iterable[str]) -> set:
        """
        Retrieve arguments of cls_obj methods as set of strings
        Args:
            cls_obj: object that contain actual methods
            iterable: iterable containing method names to process as strings
        """
        args_set = set()
        methods = [name for name in iterable if not name.startswith('__') or name == '__init__']
        for m in methods:
            args_set.update(signature(getattr(cls_obj, m)).parameters)
        return args_set

