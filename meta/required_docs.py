class DocsRequired(type):
    def __new__(cls, name, bases, namespace):
        cls_obj = super().__new__(cls, name, bases, namespace)
        if cls_obj.__doc__ is None:
            raise TypeError('All classes must have docstrings')
        return cls_obj


if __name__ == '__main__':
    # Basic test

    class A(metaclass=DocsRequired):
        """A docstring"""
        def __init__(self):
            print('Instance of A created')

    try:
        class B(A):
            ...
    except TypeError:
        print('Class B didn\'t declared because it has no docstring')
    a = A()
