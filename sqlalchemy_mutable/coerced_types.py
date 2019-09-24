"""Coerced types

Coerced types allow Mutable objects to be set to a value of the subclassed type. Unlike tracked types, attributes and items of Mutable objects will not be
converted to coerced types.
"""

from .mutable import Mutable
from .model_shell import ModelShell

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

# @Mutable.register_coerced_type(ModelShell)
# class CoercedModelShell(Mutable, ModelShell):
    # pass