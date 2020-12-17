"""# Mutable dictionary

Notes
-----
In the setup code, we use a `MutableType` database column, which handles 
dictionaries as well as other objects. To force the column to be a 
dictionary, substitute `MutableDictType` or `MutableDictJSONType` for 
`MutableType`.

Examples
--------
Make sure you have run the [setup code](setup.md).

```python
model = MyModel()
model.mutable = {}
session.add(model)
session.commit()
# without a mutable dictionary,
# this change will not survive a commit
model.mutable['hello'] = 'world'
session.commit()
model.mutable
```

Out:

```
{'hello': 'world'}
```
"""

from .mutable import Mutable
from .model_shell import ModelShell

from sqlalchemy.types import JSON, PickleType


class MutableDictType(PickleType):
    """
    Mutable dictionary database type with pickle serialization.
    """
    pass


class MutableDictJSONType(JSON):
    """
    Mutable dictionary database type with JSON serialization.
    """
    pass



@Mutable.register_tracked_type(dict)
class MutableDict(Mutable, dict):
    """Subclasses `dict`, and implements all `dict` methods.
    
    Parameters
    ----------
    source : dict, default={}
        Source object which will be converted into a mutable dictionary.

    root : sqlalchemy_mutable.Mutable or None, default=None
        Root mutable object. If `None`, `self` is assumed to be the root.
    """
    @classmethod
    def coerce(cls, key, obj):
        """Object must be dict"""
        if isinstance(obj, cls):
            return obj
        if isinstance(obj, dict):
            return cls(obj)
        return super().coerce(obj)

    # MutableDict has the following responsibilities:
    # 1. Overload getstate and setstate for pickling
    # 2. Register changes for dict methods
    # 3. Unshell models when returning values and items iterators
    def __init__(self, source={}, root=None):
        super().__init__(self._convert_mapping(source))
        
    @property
    def _tracked_items(self):
        return super().values()
    
    # 1. Pickling
    
    # Note: _mapping is the key: value mapping of the dictionary. It is used 
    # only when pickling, and is therefore not a tracked attribute.
    _untracked_attr_names = Mutable._untracked_attr_names + ['_mapping']
    
    def __getstate__(self):
        self._mapping = dict(self)
        return super().__getstate__()
    
    def __setstate__(self, state):
        self.update(state.pop('_mapping'))
        super().__setstate__(state)
    
   # 2. Register changes for dict methods
    def clear(self):
        self._changed()
        super().clear()

    def pop(self, *key_and_default):
        self._changed()
        return super().pop(*key_and_default)

    def popitem(self):
        self._changed()
        return super().popitem()

    def update(self, source={}):
        self._changed()
        super().update(self._convert_mapping(source))

    def setdefault(self, key, default=None):
        if key in self:
            return self[key]

        # this calls __setitem__, which converts the value and calls changed()
        self[key] = default
        # the value at self[key] may be a new TrackedObject, 
        # so return self[key] instead of default
        return self[key]
    
    # 3. Unshell models when returning values and items iterators
    def values(self):
        return self.unshell().values()
    
    def items(self):
        return self.unshell().items()
    
    def unshell(self):
        """
        Call to force values to unshell. Normally this occurs automatically.

        Returns
        -------
        copy : dict
            Shallow copy of `self` where all `ModelShell` values are unshelled.
        """
        return {
            key: val.unshell() if isinstance(val, ModelShell) else val
            for key, val in super().items()
        }


MutableDict.associate_with(MutableDictType)
MutableDict.associate_with(MutableDictJSONType)