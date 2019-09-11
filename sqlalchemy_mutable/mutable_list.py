"""Mutable List class and MutableListType database type

Defines the classes for (nested) mutable lists.
"""

from .mutable import Mutable
from sqlalchemy.types import PickleType


@Mutable.register_tracked_type(list)
class MutableList(Mutable, list):
    def __init__(self, iterable=(), root=None):
        self.root = root
        tracked_item_indices = range(len(iterable))
        super().__init__(
            root, (), tracked_item_indices, self._convert_iterable(iterable))
        
    def _convert_iterable(self, iterable):
        return (self._convert(item, self.root) for item in iterable)
    
    def append(self, item):
        self.changed()
        super().append(self._convert(item, self.root))

    def extend(self, iterable):
        super().extend(self.convert_iterable(iterable))

    def remove(self, obj):
        self.changed()
        return super().remove(obj)

    def pop(self, index):
        self.changed()
        return super().pop(index)

    def sort(self, cmp=None, key=None, reverse=False):
        self.changed()
        super().sort(cmp=cmp, key=key, reverse=reverse)