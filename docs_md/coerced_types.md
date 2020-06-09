<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

<link rel="stylesheet" href="https://assets.readthedocs.org/static/css/readthedocs-doc-embed.css" type="text/css" />

<style>
    a.src-href {
        float: right;
    }
    p.attr {
        margin-top: 0.5em;
        margin-left: 1em;
    }
    p.func-header {
        background-color: gainsboro;
        border-radius: 0.1em;
        padding: 0.5em;
        padding-left: 1em;
    }
    table.field-table {
        border-radius: 0.1em
    }
</style># Coerced types

Coerced types allow `Mutable` objects to be set to a value of the subclassed
type. Unlike tracked types, attributes and items of `Mutable` objects will not
be converted to coerced types.

Supported coerced types are:

- `complex`
- `float`
- `int`
- `str`
- `datetime.datetime`

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

####Examples

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
    __tablename__ = 'mymodel'
    id = Column(Integer, primary_key=True)
    greeting = Column(String)

    # initialize a database column with `MutableType`
    mutable = Column(MutableType)
    # add a query class attribute initialized with a scoped_session
    # not necessary for use with Flask-SQLAlchemy
    query = Query(Session)

    def __init__(self):
        # set mutable column to `Mutable` object
        self.mutable = Mutable()

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