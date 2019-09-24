"""Mutable List class and MutableListType database type

Defines the classes for (nested) mutable lists.
"""

from .mutable import Mutable
from sqlalchemy.types import PickleType


@Mutable.register_tracked_type(list)
class MutableList(Mutable, list):
    def __init__(self, source=[], root=None):
        super().__init__(self._convert_iterable(source))
    
    @property
    def _tracked_items(self):
        return list(self)
    
    def append(self, item):
        self._changed()
        super().append(self._convert(item, self.root))

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