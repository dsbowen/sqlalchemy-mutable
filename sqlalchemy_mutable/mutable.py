"""Mutable object base class and MutableType database type

Defines the base for (nested) mutable database objects and column type.
"""

from .model_shell import ModelShell
from sqlalchemy.types import PickleType
from sqlalchemy.ext.mutable import Mutable as MutableBase


class Mutable(MutableBase):
    """Base class for (nested) mutable objects
    
    Mutable has the following responsibilities:
    1. Register, coerce, and convert tracked types
    2. Change tracking
    3. Attribute and item management (set, get, delete)
    4. State management (for pickling and unpickling)
    """

    """1. Register, coerce, and convert tracked types"""    
    _tracked_type_mapping = {}
    _untracked_attr_names = [
        'root', '_root', '__dict__', '_tracked_type_mapping',
        '_tracked_attr_names', '_tracked_item_keys']
    
    @classmethod
    def register_tracked_type(cls, origin_type):
        """Decorator for tracked type registration
        
        The origin_type maps to a tracked_type. Origin types will be converted
        to tracked types using the convert() method. Conversion occurs
        automatically on coersion and when setting attributes and items.
        """
        def register(tracked_type):
            cls._tracked_type_mapping[origin_type] = tracked_type
            return tracked_type
        return register
    
    @classmethod
    def coerce(cls, key, obj):
        """Coercion will succeed if converted object is Mutable"""
        converted_obj = cls._convert(obj)
        if isinstance(converted_obj, cls):
            return converted_obj
        return super().coerce(key, obj)
    
    @classmethod
    def _convert(cls, obj, root=None):
        """Convert object to tracked type or ModelShell
        
        Cases:
        1. Object is database model ==> convert to ModelShell
        2. Object type is registered ==> convert to tracked type
        3. Object is Mutable ==> set root and return object
        3. Else ==> return object
        """
        if cls._object_is_model(obj):
            return ModelShell(obj)
        tracked_type = cls._tracked_type_mapping.get(type(obj))
        if tracked_type is not None:
            return tracked_type(obj, root)
        if isinstance(obj, Mutable):
            obj._set_root(root)
        return obj
    
    @classmethod
    def _object_is_model(self, obj):
        """
        Object is assumed to be a database model if it has a __table__ 
        attribute.
        """
        return hasattr(obj, '__table__')
    
    """2. Change tracking"""
    def __init__(
            self, root=None, tracked_attr_names=(), tracked_item_keys=(),
            *args, **kwargs):
        self.root = root
        self._tracked_attr_names = set(tracked_attr_names)
        self._tracked_item_keys = set(tracked_item_keys)
        super().__init__(*args, **kwargs)
    
    @property
    def root(self):
        """Get root Mutable object
        
        If the _root attribute does not yet exist, then the column is in the
        process of being unpickled. This is indicated by returning None.
        
        If _root is None, self is the root Mutable object.
        """
        if not hasattr(self, '_root'):
            return
        root = self if self._root is None else self._root
        return root
    
    @root.setter
    def root(self, root):
        self._root = root
        
    @property
    def _tracked_children(self):
        """Return a list of all tracked children (attributes and items)"""
        tracked_children = [
            self.__getattribute__(name) for name in self._tracked_attr_names]
        tracked_children.extend([
            self.__getitem__(key) for key in self._tracked_item_keys])
        return tracked_children
    
    def _set_root(self, root=None):
        """Set the root for self and Mutable tracked children"""
        self.root = root
        [child._set_root(self.root) for child in self._tracked_children
            if isinstance(child, Mutable)]
    
    def _changed(self):
        """Mark the root Mutable object as changed
        
        Root will be None during unpickling. In this case, no change is 
        necessary (or possible).
        """
        if self.root is None:
            return
        Mutable.changed(self.root)
    
    """3. Attribute and item management"""
    def __setattr__(self, name, obj):
        if name in self._untracked_attr_names:
            return super().__setattr__(name, obj)
        self._changed()
        self._tracked_attr_names.add(name)
        super().__setattr__(name, self._convert(obj, self.root)) 

    def __getattribute__(self, name):
        obj = super().__getattribute__(name)
        if isinstance(obj, ModelShell):
            return obj.unshell()
        return obj
    
    def __delattr__(self, name):
        self._changed()
        self._tracked_attr_names.remove(name)
        super().__delattr__(name)
    
    def __setitem__(self, key, obj):
        self._changed()
        self._tracked_item_keys.add(key)
        super().__setitem__(key, self._convert(obj, self.root))
    
    def __getitem__(self, key):
        obj = super().__getitem__(key)
        if isinstance(obj, ModelShell):
            return obj.unshell()
        return obj
    
    def __delitem__(self, key):
        self._changed()
        self._tracked_item_keys.remove(key)
        super().__delitem__(key)
    
    """4. State management (for pickling and unpickling)"""
    def __getstate__(self):
        """Get state for pickling
        
        State is self.__dict__ but with `_root` replaced by an `isroot`
        indicator.
        """
        state = self.__dict__.copy()
        state.pop('_parents', None)
        state.pop('_root', None)
        state['isroot'] = self == self.root
        return state
    
    def __setstate__(self, state):
        """
        If self is the root Mutable object, set the root for self 
        and all tracked Mutable children.
        """
        isroot = state.pop('isroot', None)
        self.__dict__ = state
        if isroot:
            self._set_root()


class MutableType(PickleType):
    """Mutable database type"""
    

Mutable.associate_with(MutableType)