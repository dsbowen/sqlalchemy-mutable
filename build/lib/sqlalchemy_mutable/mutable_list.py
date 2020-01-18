"""Mutable List class and MutableListType database type

Defines the classes for (nested) mutable lists.
"""

from .mutable import Mutable
from .model_shell import ModelShell

from sqlalchemy.types import PickleType


@Mutable.register_tracked_type(list)
class MutableList(Mutable, list):
    """Mutbale list object
    
    MutableList has the following responsibilities:
    1. Overload getstate and setstate for pickling
    2. Register changes for list methods
    3. Unshell models when returning list iterator
    """
    def __init__(self, source=[], root=None):
        """
        _pickling indicates that the MutableList is being pickled. When 
        creating the list iterable during pickling, ModelShell objects 
        should not be unshelled.
        """
        self._pickling = False
        super().__init__(self._convert_iterable(source))
    
    @property
    def _tracked_items(self):
        return list(self)

    """1. Pickling
    
    Note: _mapping is the index: value mapping of the list. It is used 
    only when pickling, and is therefore not a tracked attribute.
    """
    _untracked_attr_names = (
        Mutable._untracked_attr_names + ['_mapping', '_pickling'])

    def __getstate__(self):
        self._pickling = True
        self._mapping = list(self)
        return super().__getstate__()
    
    def __setstate__(self, state):
        super().__setstate__(state)
        self._pickling = False
    
    """2. Register changes for list methods"""
    def append(self, item):
        self._changed()
        super().append(self._convert_item(item))

    def clear(self):
        self._changed()
        super().clear()

    def extend(self, iterable):
        self._changed()
        super().extend(self._convert_iterable(iterable))

    def remove(self, obj):
        self._changed()
        return super().remove(obj)

    def pop(self, index):
        self._changed()
        return super().pop(index)

    def sort(self, cmp=None, key=None, reverse=False):
        self._changed()
        super().sort(cmp=cmp, key=key, reverse=reverse)
    
    """3. Unshell models when returning list iterator"""
    def __iter__(self):
        """
        Note: ModelShells should not be unshelled when pickling.
        """
        for i in super().__iter__():
            if not self._pickling and isinstance(i, ModelShell):
                yield i.unshell()
            else:
                yield i


class MutableListType(PickleType):
    """Mutable list database type"""
    @classmethod
    def coerce(cls, key, obj):
        """Object must be list"""
        if isinstance(obj, cls):
            return obj
        if isinstance(obj, list):
            return cls(obj)
        return super().coerce(obj)


MutableList.associate_with(MutableListType)