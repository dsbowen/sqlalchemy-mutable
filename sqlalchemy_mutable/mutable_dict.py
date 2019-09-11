"""Mutable Dict class and MutableDictType database type

Defines the classes for (nested) mutable dictionaries.
"""

from .mutable import Mutable
from sqlalchemy.types import PickleType


@Mutable.register_tracked_type(dict)
class MutableDict(Mutable, dict):
    _untracked_attr_names = Mutable._untracked_attr_names + ['_mapping']

    def __init__(self, source={}, root=None, **kwargs):
        self.root = root
        tracked_item_keys = source.keys()
        super().__init__(root, self._convert_mapping(source))
        
    @property
    def _tracked_items(self):
        return self.values()
    
    def __getstate__(self):
        self._mapping = dict(self)
        return super().__getstate__()
    
    def __setstate__(self, state):
        self.update(state.pop('_mapping'))
        super().__setstate__(state)
    
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
        super().update(source)

    def setdefault(self, key, default=None):
        if key in self:
            return self[key]

        # this calls __setitem__, which converts the value and calls changed()
        self[key] = default
        # the value at self[key] may be a new TrackedObject, 
        # so return self[key] instead of default
        return self[key]


class MutableDictType(PickleType):
    """Mutable dictionary database type"""
    @classmethod
    def coerce(cls, key, obj):
        """Object must be dict"""
        if isinstance(obj, cls):
            return obj
        if isinstance(obj, dict):
            return cls(obj)
        return super().coerce(obj)


MutableDict.associate_with(MutableDictType)