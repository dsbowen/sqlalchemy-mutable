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
    1. Register changes for list methods
    2. Unshell models when returning list iterator
    """
    def __init__(self, source=[], root=None):
        super().__init__(self._convert_iterable(source))
    
    @property
    def _tracked_items(self):
        return list(self)
    
    """1. Register changes for list methods"""
    def append(self, item):
        self._changed()
        super().append(self._convert_item(item))

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
    
    """2. Unshell models when returning list iterator"""
    def __iter__(self):
        for i in super().__iter__():
            if isinstance(i, ModelShell):
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