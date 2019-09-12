"""sqlalchemy-mutable

Support for generic nested mutable objects and iterables.

Create custom mutable objects by subclassing Mutable. 

Convert existing objects to mutable objects using the
@Mutable.register_tracked_type decorator. See implementation of MutableList
and MutableDict for examples.

sqlalchemy-json deserves much credit for inspiring this project.
"""


from .model_shell import Query
from .mutable import Mutable, MutableType
from .mutable_list import MutableList, MutableListType
from .mutable_dict import MutableDict, MutableDictType