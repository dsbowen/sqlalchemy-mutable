"""Coerced types

Coerced types allow Mutable objects to be set to a value of the subclassed type. Unlike tracked types, attributes and items of Mutable objects will not be
converted to coerced types.
"""

from .model_shell import ModelShell
from .mutable import Mutable

from datetime import datetime

@Mutable.register_coerced_type(ModelShell)
class CoercedModelShell(Mutable, ModelShell):
    def __init__(self, source):
        self.id = source.id
        self.model_class = source.model_class

@Mutable.register_coerced_type(complex)
class CoerceComplex(Mutable, complex):
    pass

@Mutable.register_coerced_type(float)
class CoercedFloat(Mutable, float):
    pass
    
@Mutable.register_coerced_type(int)
class CoercedInt(Mutable, int):
    pass

@Mutable.register_coerced_type(str)
class CoercedStr(Mutable, str):
    pass

@Mutable.register_coerced_type(datetime)
class CoercedDatetime(Mutable, datetime):
    def __new__(cls, source):
        if isinstance(source, datetime):
            return datetime.__new__(
                cls,
                source.year,
                source.month,
                source.day,
                source.hour,
                source.minute,
                source.second,
                source.microsecond,
                source.tzinfo,
                fold=source.fold
            )
        return super().__new__(cls, source)