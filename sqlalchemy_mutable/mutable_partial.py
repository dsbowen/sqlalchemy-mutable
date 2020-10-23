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


class partial(Mutable):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        assert callable(func), 'First argument must be callable'
        self._python_type = None
        self.func, self.args, self.kwargs = func, list(args), kwargs

    def __call__(self, *args, **kwargs):
        if self.func is not None:
            # kwargs is mutable dictionary, args is mutable list
            kwargs_ = self.kwargs.unshell()
            kwargs_.update(kwargs)
            return self.func(*args, *self.args.unshell(), **kwargs_)

    def __repr__(self):
        args_str = ', '.join([i.__repr__() for i in self.args])
        kwargs_str = ', '.join([
            '{}={}'.format(key, val.__repr__()) 
            for key, val in self.kwargs.items()
        ])
        args_kwargs_str = ''
        if args_str and kwargs_str:
            args_kwargs_str = args_str + ', ' + kwargs_str
        elif args_str and not kwargs_str:
            args_kwargs_str = args_str
        elif not args_str and kwargs_str:
            args_kwargs_str = kwargs_str
        return '<{}({})>'.format(self.func.__name__, args_kwargs_str)

    @classmethod
    def register(cls, func):
        def add_function(*args, **kwargs):
            return cls(func, *args, **kwargs)

        setattr(cls, func.__name__, add_function)
        return func