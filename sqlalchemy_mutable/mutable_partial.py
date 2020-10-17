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


@Mutable.register_tracked_type(partial)
class _MutablePartial(partial, Mutable):
    def __init__(self, source=None, root=None):
        super().__init__(source.func, *source.args, **source.kwargs)