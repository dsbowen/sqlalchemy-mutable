# Setup

All examples in the documentation assume you have run the following setup code for [SQLAlchemy](https://www.sqlalchemy.org/) or [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/).

## SQLAlchemy

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

## Flask-SQLAlchemy

```python
from sqlalchemy_mutable import Mutable, MutableType, MutableModelBase

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create a session (standard)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# subclass `MutableModelBase` when creating database models
class MyModel(MutableModelBase, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    greeting = db.Column(db.String)
    
    # initialize a database column with `MutableType`
    mutable = db.Column(MutableType)  
    
    def __init__(self):
        # set mutable column to `Mutable` object
        self.mutable = Mutable()

# create the database (standard)
db.create_all()
session = db.session
```