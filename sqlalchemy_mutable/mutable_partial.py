"""# Mutable partial

This is analogous to `functools.partial`.

Examples
--------
Make sure you have run the [setup code](setup.md).

```python
def foo(*args, **kwargs):
\    print('args', args)
\    print('kwargs', kwargs)
\    return 0

model = MyModel()
model.mutable = partial(foo, 'hello world', goodbye='moon')
model.mutable()
```

Out:

```
args ('hello world',)
kwargs {'goodbye': 'moon'}
0
```
"""

from .mutable import Mutable


class partial():
    def __init__(self, func, *args, **kwargs):
        assert callable(func), 'First argument must be callable'
        self.func, self.args, self.kwargs = func, list(args), kwargs

    @classmethod
    def register(cls, func):
        """
        Register a partial function.

        Parameters
        ----------
        func : callable

        Returns
        -------
        func : callable
            `func` parameter.

        Examples
        --------
        Make sure you have run the setup code.

        ```python
        @partial.register
        def foo(*args, **kwargs):
        \    print('args', args)
        \    print('kwargs', kwargs)
        \    return 0

        model = MyModel()
        model.mutable = partial.foo('hello world', goodbye='moon')
        model.mutable()
        ```
        """
        def add_function(*args, **kwargs):
            return cls(func, *args, **kwargs)

        setattr(cls, func.__name__, add_function)
        return func


@Mutable.register_tracked_type(partial)
class _MutablePartial(partial, Mutable):
    def __init__(self, source=None, root=None):
        super().__init__(source.func, *source.args, **source.kwargs)

    def __call__(self, *args, **kwargs):
        if self.func is not None:
            # kwargs is mutable dictionary, args is mutable list
            kwargs_ = self.kwargs.unshell()
            kwargs_.update(kwargs)
            return self.func(*args, *self.args.unshell(), **kwargs_)