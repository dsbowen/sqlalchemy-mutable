"""Mutable object, Column type, and model base

Defines the core classes for SQLAlchemy-Mutable. 

Mutable is a generic mutable object which tracks changes to its children.

MutableType database Columns may be set to a Mutable object (including 
MutableList and MutableDict objects), or common literals such as an integer 
or string (see coerced_types.py).

MutableType database Columns may also be set to another database model. To 
support this functionality, programmers should subclass MutableModelBase in 
any database model containing MutableType Columns which may be set to 
another database model.
"""

from .model_shell import ModelShell

from sqlalchemy.types import PickleType
from sqlalchemy.ext.mutable import Mutable as MutableBase


class Mutable(MutableBase):
    """Base class for (nested) mutable objects
    
    Mutable has the following responsibilities:
    1. Register, coerce, and convert types
    2. Change tracking
    3. Attribute and item management (set, get, delete)
    4. State management (for pickling and unpickling)
    
    Subclass this to create custom mutable objects.
    """

    """1. Register, coerce, and convert types"""    
    _coerced_type_mapping = {}
    _tracked_type_mapping = {}
    _untracked_attr_names = [
        'root', '_root', '__dict__', '_python_type', 
        '_coerced_type_mapping', '_tracked_type_mapping',
        '_tracked_attr_names', '_tracked_item_keys']
    
    @classmethod
    def register_coerced_type(cls, origin_type):
        """Decorator for coerced type registration
        
        The origin_type maps to a coerced_type. Objects of origin types will be converted to objects of coerced types when the coerce method is invoked. Objects of origin types will not be converted when the _convert method is invoked.
        """
        def register(coerced_type):
            cls._coerced_type_mapping[origin_type] = coerced_type
            return coerced_type
        return register
    
    @classmethod
    def register_tracked_type(cls, origin_type):
        """Decorator for tracked type registration
        
        The origin_type maps to a tracked_type. Objects of origin types will be converted to objects of tracked types when the convert method is invoked. Conversion occurs automatically on coersion and when 
        setting attributes and items.
        """
        def register(tracked_type):
            cls._tracked_type_mapping[origin_type] = tracked_type
            return tracked_type
        return register
    
    @classmethod
    def coerce(cls, key, obj):
        """Coercion
        
        If object can be converted to a Mutable object, return the Mutable
        object. Otherwise, attempt to coerce to a coerced_type.
        """
        converted_obj = cls._convert(obj)
        if isinstance(converted_obj, cls):
            return converted_obj
        coerced_type = cls._coerced_type_mapping.get(type(converted_obj))
        if coerced_type is not None:
            return coerced_type(converted_obj)
        return super().coerce(cls, obj)
    
    @classmethod
    def _convert(cls, obj, root=None):
        """Convert object to tracked type or ModelShell
        
        Cases:
        1. Object is database model ==> convert to ModelShell
        2. Object type is registered as tracked ==> convert to tracked type
        3. Object is Mutable ==> set root and return object
        3. Else ==> return object
        """
        if cls._object_is_model(obj):
            return ModelShell(obj)
        tracked_type = cls._tracked_type_mapping.get(type(obj))
        if tracked_type is not None:
            return tracked_type(obj, root)
        if isinstance(obj, Mutable):
            obj.root = root
        return obj
    
    @classmethod
    def _object_is_model(self, obj):
        """Indicates whether the object is a database model
        
        Object is assumed to be a database model if it has a __table__ 
        attribute.
        """
        return hasattr(obj, '__table__')
    
    def _convert_item(self, item):
        """Convert a single item to Mutable object"""
        return self._convert(item, self.root)
    
    def _convert_iterable(self, iterable):
        """Convert items in iterable to Mutable objects"""
        return (self._convert_item(item) for item in iterable)
    
    def _convert_mapping(self, mapping):
        """Convert items in dictionary key:item mapping to Mutable objects"""
        return {
            key: self._convert_item(item) for key, item in mapping.items()}
    
    """2. Change tracking"""
    def __new__(cls, source=None, root=None, *args, **kwargs):
        """Create new Mutable object
        
        Begin by creating a new object of type cls using super().__new__. If 
        super().__new__ takes arguments, I assume the first argument is a 
        source object (the new methods of many literals work this way). 
        Otherwise, begin by creating an empty new object.
        
        Then set the root, python type, and empty tracked attribute names 
        registry. The root is used to register changes with the root Mutable 
        object. The python type is used to check for valid attribute setting 
        (see __setattr__). The tracked attribute registry is used for 
        assigning new root mutable objects.
        """
        try:
            new = super().__new__(cls, source)
        except:
            new = super().__new__(cls)
        new._python_type = type(source) if source is not None else None
        new._tracked_attr_names = set()
        new.root = root
        return new
    
    @property
    def root(self):
        """Get root Mutable object
        
        If the _root attribute does not yet exist, then the Column is in the
        process of being unpickled. This is indicated by returning None.
        
        If _root is None, self is the root Mutable object.
        """
        if not hasattr(self, '_root'):
            return
        root = self if self._root is None else self._root
        return root
    
    @root.setter
    def root(self, root):
        """Set root Mutable object
        
        Recursively set the root Mutable object for all tracked children.
        """
        self._root = root
        for child in self._tracked_children:
            if isinstance(child, Mutable):
                child.root = self.root
        
    @property
    def _tracked_children(self):
        """Return a list of all tracked children (attributes and items)"""
        tracked_children = [
            self.__getattribute__(name) for name in self._tracked_attr_names]
        if hasattr(self, '_tracked_items'):
            tracked_children += list(self._tracked_items)
        return tracked_children
    
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
        """Set attribute
        
        If attribute is untracked, or if self is a ModelShell, set as 
        normal. Self should only be a ModelShell when a MutableType column 
        is set to a database model. In this case, Mutable coerces it to a 
        ModelShell and stores the id and model class using __setattr__. 
        These attributes should not be tracked.
        
        If the attribute is tracked and is derived from an original python
        type, make sure instances of the original python type can set the
        requested attribute.
        
        If so, indicate that self has changed, add the attribute name to the
        tracked attribute registry, and set the attribute.
        """
        if name in self._untracked_attr_names or isinstance(self, ModelShell):
            return super().__setattr__(name, obj)
        if self._python_type is not None:
            empty = self._python_type.__new__(self._python_type)
            empty.__setattr__(name, obj)
        self._changed()
        self._tracked_attr_names.add(name)
        super().__setattr__(name, self._convert(obj, self.root)) 

    def __getattribute__(self, name):
        obj = super().__getattribute__(name)
        if isinstance(obj, ModelShell):
            return obj.unshell()
        return obj
    
    def __delattr__(self, name):
        if name in self._tracked_attr_names:
            self._changed()
            self._tracked_attr_names.remove(name)
        super().__delattr__(name)
    
    def __setitem__(self, key, obj):
        self._changed()
        super().__setitem__(key, self._convert(obj, self.root))
    
    def __getitem__(self, key):
        obj = super().__getitem__(key)
        if isinstance(obj, ModelShell):
            return obj.unshell()
        return obj
    
    def __delitem__(self, key):
        self._changed()
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
        """Set state for unpickling
        
        If self is the root Mutable object, set the root for self 
        (and all Mutable children).
        """
        isroot = state.pop('isroot', None)
        self.__dict__ = state
        if isroot:
            self.root = None


class MutableType(PickleType):
    """Mutable database type"""
    
Mutable.associate_with(MutableType)


class MutableModelBase():
    """Base for database models with MutableType columns"""
    def __getattribute__(self, name):
        """
        Sometimes programmers will set a Mutable attribute to a database 
        model. When this occurs, Mutable coerces the model into a 
        ModelShell. To retrieve the model, this method checks if a requested 
        attribute is a ModelShell, and if so returns the original model.
        
        Note that this is identical to the Mutable __getattribute__ method.
        """
        obj = super().__getattribute__(name)
        if isinstance(obj, ModelShell):
            return obj.unshell()
        return obj