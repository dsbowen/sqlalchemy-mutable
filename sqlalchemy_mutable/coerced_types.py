
from .mutable import Mutable

@Mutable.register_coerced_type(str)
class CoercedStr(Mutable, str):
    pass