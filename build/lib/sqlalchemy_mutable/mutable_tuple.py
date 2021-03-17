"""# Mutable tuple

Notes
-----
In the setup code, we use a `MutableType` database column that handles tuples
as well as other objects. To force the column to be a tuple, substitute `MutableTupleType` or `MutableTupleJSONType` for `MutableType`.

Examples
--------
Make sure you have run the [setup code](setup.md).

```python
model0 = MyModel()
model1 = MyModel()
model0.mutable = [(model1,)]
session.add_all([model0, model1])
session.commit()
# without a mutable tuple, 
# this change would not appear after a commit
model1.greeting = 'hello world'
session.commit()
model0.mutable[0][0].greeting
```

Out:

```
'hello world'
```
"""

from .mutable import Mutable
from .model_shell import ModelShell

from sqlalchemy.types import JSON, PickleType


class MutableTupleType(PickleType):
    """
    Mutable tuple database type with pickle serialization.
    """
    pass


class MutableTupleJSONType(JSON):
    """
    Mutable tuple database type with JSON serialization.
    """
    pass


@Mutable.register_tracked_type(tuple)
class MutableTuple(Mutable, tuple):
    """
    Parameters
    ----------
    source : tuple, default=()
        Source objects that will be converted into a mutable tuple.

    root : sqlalchemy.Mutable or None, default=None
        Root mutable object. If `None`, `self` is assumed to be the root.
    """
    @classmethod
    def coerce(cls, key, obj):
        if isinstance(obj, cls):
            return obj
        if isinstance(obj, tuple):
            return cls(obj)
        if not obj:
            return cls(())
        return cls((obj))

    @property
    def _tracked_items(self):
        return [i for i in self]

    def __new__(cls, source=(), root=None):
        converted = tuple((cls._convert(obj, root) for obj in source))
        return super().__new__(cls, converted)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.__class__(super().__getitem__(key))
        return super().__getitem__(key)

    def unshell(self):
        """
        Call to force values to unshell. Normally, this occurs automatically.

        Returns
        -------
        copy : tuple
            Shallow copy of `self` where all `ModelShell` items are unshelled.
        """
        return tuple(
            (i.unshell() if hasattr(i, 'unshell') else i for i in self)
        )


MutableTuple.associate_with(MutableTupleType)
MutableTuple.associate_with(MutableTupleJSONType)