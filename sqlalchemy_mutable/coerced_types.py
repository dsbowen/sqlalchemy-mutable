"""# Coerced types

Coerced types allow `Mutable` objects to be set to a value of the subclassed 
type. Unlike tracked types, attributes and items of `Mutable` objects will not 
be converted to coerced types.

Supported coerced types are:

- `bool`
- `complex`
- `datetime.datetime`
- `float`
- `int`
- `str`
- `types.FunctionType`

Examples
--------
We begin with setup as follows.

```python
from sqlalchemy_mutable import Mutable, MutableType, MutableModelBase, Query

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# create a session (standard)
engine = create_engine('sqlite:///:memory:')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()
Base = declarative_base()

# subclass `MutableModelBase` when creating database models 
# with `MutableType` columns
class MyModel(MutableModelBase, Base):
\    __tablename__ = 'mymodel'
\    id = Column(Integer, primary_key=True)
\    greeting = Column(String)
    
\    # initialize a database column with `MutableType`
\    mutable = Column(MutableType) 
\    # add a query class attribute initialized with a scoped_session
\    # not necessary for use with Flask-SQLAlchemy
\    query = Query(Session) 
    
\    def __init__(self):
\        # set mutable column to `Mutable` object
\        self.mutable = Mutable()

# create the database (standard)
Base.metadata.create_all(engine)
```

String example.

```python
model = MyModel()
model.mutable = 'hello world'
model.mutable
```

Out:

```
'hello world'
```
"""

from .model_shell import ModelShell
from .mutable import Mutable

import types
from datetime import datetime

@Mutable.register_coerced_type(ModelShell)
class CoercedModelShell(Mutable, ModelShell):
    def __init__(self, source):
        self.id = source.id
        self.model_class = source.model_class

@Mutable.register_coerced_type(bool)
class CoercedBool(Mutable):
    def __new__(cls, source=None):
        new = super().__new__(cls)
        new.value = source
        return new

@Mutable.register_coerced_type(complex)
class CoercedComplex(Mutable, complex):
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

@Mutable.register_coerced_type(types.FunctionType)
class CoercedFunc(Mutable):
    def __new__(cls, source=None):
        new = super().__new__(cls)
        new.func = source
        return new
    
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

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