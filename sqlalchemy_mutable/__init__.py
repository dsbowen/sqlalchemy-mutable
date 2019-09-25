"""sqlalchemy-mutable

Support for generic nested mutable objects and iterables.

sqlalchemy-json deserves much credit for inspiring this project.
"""

from .model_shell import Query
from .mutable import Mutable, MutableType, MutableModelBase
from .mutable_dict import MutableDict, MutableDictType
from .mutable_list import MutableList, MutableListType
from .coerced_types import *