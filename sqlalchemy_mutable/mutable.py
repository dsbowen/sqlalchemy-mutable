"""Mutable object base and MutableType database type

Defines the base for (nested) mutable database objects and column type.
"""

from .model_shell import ModelShell
from sqlalchemy.inspection import inspect
from sqlalchemy.ext import Mutable as MutableBase


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
    
    