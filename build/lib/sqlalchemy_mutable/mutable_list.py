"""# Mutable list

Notes
-----
In the setup code, we use a `MutableType` database column, which handles 
lists as well as other objects. To force the column to be a list, 
substitute `MutableListType` or `MutableListJSONType` for `MutableType`. 

Examples
--------
Make sure you have run the [setup code](setup.md).

```python
model = MyModel()
model.mutable = []
session.add(model)
session.commit()
# without a mutable list,
# this change will not survive a commit
model.mutable.append('hello world')
session.commit()
model.mutable
```

Out:

```
['hello world']
```
"""

from .mutable import Mutable
from .model_shell import ModelShell

from sqlalchemy.types import JSON, PickleType


class MutableListType(PickleType):
    """
    Mutable list database type with pickle serialization.
    """
    pass


class MutableListJSONType(JSON):
    """
    Mutable list database type with JSON serialization.
    """
    pass


@Mutable.register_tracked_type(list)
class MutableList(Mutable, list):
    """Subclasses `list`, and implements all `list` methods.
    
    Parameters
    ----------
    source : list, default=[]
        Source objects which will be converted into a mutable list.

    root : sqlalchemy.Mutable or None, default=None
        Root mutable object. If `None`, `self` is assumed to be the root.
    """
    @classmethod
    def coerce(cls, key, obj):
        """Object must be list or None"""
        if isinstance(obj, cls):
            return obj
        if isinstance(obj, list):
            return cls(obj)
        if not obj:
            return cls([])
        return cls([obj])

    def __init__(self, source=[], root=None):
        """
        _pickling indicates that the MutableList is being pickled. When 
        creating the list iterable during pickling, ModelShell objects 
        should not be unshelled.
        """
        super().__init__(self._convert_iterable(source))
    
    @property
    def _tracked_items(self):
        return list(self)
    
    def __iadd__(self, items):
        self._changed()
        return super().__iadd__(self._convert_iterable(items))

    def __imul__(self, val):
        self._changed()
        return super().__imul__(val)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.__class__(super().__getitem__(key))
        return super().__getitem__(key)

    def __setitem__(self, key, items):
        self._changed()
        if isinstance(key, slice):
            items = self._convert_iterable(items)
        else:
            items = self._convert_item(items)
        return super().__setitem__(key, items)

    def append(self, item):
        self._changed()
        return super().append(self._convert_item(item))

    def clear(self):
        self._changed()
        return super().clear()

    def extend(self, iterable):
        self._changed()
        return super().extend(self._convert_iterable(iterable))

    def remove(self, obj):
        self._changed()
        return super().remove(obj)

    def reverse(self):
        self._changed()
        return super().reverse()

    def pop(self, index):
        self._changed()
        return super().pop(index)

    def sort(self, key=None, reverse=False):
        self._changed()
        return super().sort(key=key, reverse=reverse)
    
    def unshell(self):
        """
        Call to force values to unshell. Normally this occurs automatically.

        Returns
        -------
        copy : list
            Shallow copy of `self` where all `ModelShell` items are unshelled.
        """
        return [i.unshell() if hasattr(i, 'unshell') else i for i in self]


MutableList.associate_with(MutableListType)
MutableList.associate_with(MutableListJSONType)