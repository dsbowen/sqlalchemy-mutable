SQLAlchemy-Mutable aspires to be the most powerful and flexible [SQLAlchemy](https://www.sqlalchemy.org) database column type.

Its features include:

1. Nested mutation tracking
2. Mutation tracking for `list` and `dict`
3. Support for storing database models in mutable columns
4. Support for common literals and `datetime` objects
5. Support for custom mutable classes
6. Support for converting existing classes to mutable classes

## Installation

```
$ pip install sqlalchemy-mutable
```

## Quickstart

Setup:

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
# which may be stored in a `Mutable` object
class MyModel(MutableModelBase, Base):
    __tablename__ = 'mymodel'
    id = Column(Integer, primary_key=True)
    greeting = Column(String)
    
    # initialize a database column with `MutableType`
    mutable = Column(MutableType) 
    # add a `query` class attribute initialized with a scoped_session
    # not necessary for use with Flask-SQLAlchemy
    query = Query(Session) 
    
    def __init__(self):
        # set mutable column to `Mutable` object
        self.mutable = Mutable()

# create the database (standard)
Base.metadata.create_all(engine)
```

Examples:

```python
model = MyModel()
session.add(model)
session.commit()

# nested mutable objects
model.mutable.nested_mutable = Mutable()
session.commit()
model.mutable.nested_mutable.greet = 'hello world'
session.commit()
print(model.mutable.nested_mutable.greet)

# nested mutable list and dict
model.mutable = {}
session.commit()
model.mutable['greet'] = ['hello world']
session.commit()
print(model.mutable)

# storing database models
model.mutable = model
session.commit()
print(model.mutable)

# common literals
model.mutable = 'hello world'
session.commit()
print(model.mutable)
```

Out:

```
hello world
{'greet': ['hello world']}
<__main__.MyModel object at 0x7fe54a2d7b00>
hello world
```

## Citation

```
@software{bowen2020sqlalchemy-mutable,
  author = {Dillon Bowen},
  title = {SQLAlchemy-Mutable},
  url = {https://dsbowen.github.io/sqlalchemy-mutable/},
  date = {2020-10-16},
}
```

## License

Users must cite this package in any publications which use it.

It is licensed with the MIT [License](https://github.com/dsbowen/sqlalchemy-mutable/blob/master/LICENSE).

## Acknowledgments

Original inspiration drawn from [SQLAlchemy-JSON](https://github.com/edelooff/sqlalchemy-json).