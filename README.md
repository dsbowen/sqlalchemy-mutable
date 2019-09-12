# SQLAlchemy-Mutable

SQLAlchemy-Mutable provides generic nested mutable objects and iterables for [SQLAlchemy](https://www.sqlalchemy.org). Its primary features are:

1. Nested mutation tracking
2. Mutation tracking for iterables (```list``` and ```dict```)
3. Support for embedded database models
4. ```Mutable``` base for customized mutable classes
5. Support for converting existing classes to mutable classes

## Getting Started

### Installation

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart):

```
$ pip install -U sqlalchemy-mutable
```

### Setup

Import classes from sqlalchemy_mutable

```python
from sqlalchemy_mutable import Mutable, MutableType, Query
```

Setup the SQLAlchemy [session](https://docs.sqlalchemy.org/en/13/orm/session_basics.html) (standard)

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///:memory:')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()
Base = declarative_base()

class MyModel(Base):
    __tablename__ = 'mymodel'
    id = Column(Integer, primary_key=True)
    greeting = Column(String)
```

Initialize a database column with ```MutableType``` (or ```MutableListType``` or ```MutableDictType```)

```python
class MyModel(Base):
    # ...
    mutable = Column(MutableType)
```

Add a ```query``` class attribute initialized with a [```scoped_session```](https://docs.sqlalchemy.org/en/13/orm/contextual.html#sqlalchemy.orm.scoping.scoped_session) object (skip this step if using with [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/))

```python
class MyModel(Base):
    # ...
    query = Query(Session)
```

Set ```mutable``` column to ```Mutable``` object

```python
class MyModel(Base):
    # ...
    def __init__(self):
        self.mutable = Mutable()
```

Create the database (standard)

```python
Base.metadata.create_all(engine)
```

## Examples

See full examples with [SQLAlchemy](https://github.com/dsbowen/sqlalchemy-mutable/blob/master/examples.py) and [Flask-SQLAlchemy](https://github.com/dsbowen/sqlalchemy-mutable/blob/master/flask_sqlalchemy_examples.py)

### Example 1: Nested mutation tracking

```MutableType``` columns track changes made to nested ```Mutable``` objects.

```python
x = MyModel()
session.add(x)
x.mutable.nested_mutable = Mutable()
session.commit()
x.mutable.nested_mutable.greeting = 'hello world'
session.commit()
print(x.mutable.nested_mutable.greeting)
```

Outputs:

```
hello world
```

### Example 2: Mutation tracking for iterables

SQLAlchemy-Mutable also supports mutation tracking for nested iterables (```list``` and ```dict```)

```python
x = MyModel()
session.add(x)
x.mutable = {'greeting': []}
session.commit()
x.mutable['greeting'].append('hello world')
session.commit()
print(x.mutable['greeting'][0])
```

Outputs:

```
hello world
```

### Example 3: Embedded database models

Database models may be embedded in the ```Mutable``` object.

**Note:** Embedded database models must be flushed or committed before embedding.

```python
x = MyModel()
y = MyModel()
session.add_all([x,y])
session.flush([x,y]) # Flush or commit models before embedding
x.mutable.y = y
session.commit()
y.greeting = 'hello world'
print(x.mutable.y.greeting)
print('Successfully recovered y?', x.mutable.y == y)
```

Outputs:

```
hello world
Successfully recovered y? True
```

### Example 4: ```Mutable``` base for customized mutable classes

Users can define custom mutable classes by subclassing ```Mutable```.

**Note:** Custom ```__init__``` function must begin by calling```super().__init__()```.

```python
class CustomMutable(Mutable):
    def __init__(self, name='world'):
        super().__init__() # Begin by calling super().__init__()
        self.name = name
        
    def greeting(self):
        return 'hello {}'.format(self.name)

x = MyModel()
x.mutable.nested_mutable = CustomMutable()
session.commit()
print(x.mutable.nested_mutable.greeting())
x.mutable.nested_mutable.name = 'moon'
session.commit()
print(x.mutable.nested_mutable.greeting())
```

Outputs:

```
hello world
hello moon
```

### Example 5.1: Convert existing classes to mutable classes (basic use)

Users can add mutation tracking to existing classes. The basic steps are:
1. Create a new mutable class which inherits from ```Mutable``` and the existing class.
2. Associate the new mutable class with the existing class by registering it using ```@Mutable.register_tracked_type(<Existing Class>)```.
3. Define ```__init__``` for the new mutable class. ```__init__``` takes a ```source``` (an instance of the existing class type) and a ```root``` (the ```Mutable``` instance at the root of the nested mutable structure, default to ```None```).
    1. Assign the root with ```self.root=root```.
    2. Collect the arguments and keyworks arguments of the existing class constructor from ```source```.
    3. Call ```super().__init__(root, <arguments>)``` where the arguments following ```root``` are those you collected in 3.2. This calls the existing class constructor with the collected arguments.

You can now treat the existing class as if it were mutable.

```python
class ExistingClass():
    def __init__(self, name):
        self.name = name
        print('My name is', self.name)
    
    def greeting(self):
        return 'hello {}'.format(self.name)

# 1. Create new mutable class which inherits from Mutable and ExistingClass
# 2. Registration
@Mutable.register_tracked_type(ExistingClass)
class MutableClass(Mutable, ExistingClass):
    # 3. Initialization
    def __init__(self, source=(), root=None):
        self.root = root
        src_name = source.name if hasattr(source, 'name') else None
        print('source name is', src_name)
        super().__init__(root, name=src_name)
        
x = MyModel()
session.add(x)
x.mutable.nested_mutable = ExistingClass('world')
session.commit()
print(x.mutable.nested_mutable.greeting())
x.mutable.nested_mutable.name = 'moon'
session.commit()
print(x.mutable.nested_mutable.greeting())
```

Outputs:

```
My name is world
source name is world
My name is world
hello world
hello moon
```

### Example 5.2: Convert existing classes to mutable classes (advanced use)

Notes for converting more complex existing classes to mutable classes:
1. *Existing class methods take (potentially) mutable arguments*. Convert existing class method arguments to ```Mutable``` objects before passing to the existing class method with ```super().<method>(<converted arguments>)```. ```Mutable``` provides convenience methods for converting arguments:
    1. ```_convert(object, root=None)``` converts a single object.
    2. ```_convert_iterable(iterable)``` converts iterables like ```list```.
    3. ```_convert_mapping(mapping)``` converts key:value mappings like ```dict```.
2. *The existing class contains items other than its attributes whose mutations you want to track*. For example, a ```list``` contains potentially mutable items which are not attributes. In this case, the new mutable class must have a ```_tracked_items``` attribute which lists these items.
3. *The existing class has methods which mutate the object but do not call ```__setattr___```, ```___delattr___```, ```___setitem___```, or ```__delitem__```*. The new mutable class must redefine these methods to call ```self._changed()``` in addition to the existing class method ```super().<method>()```.

```python
@Mutable.register_tracked_type(list) 
class MutableList(Mutable, list):
    def __init__(self, source=(), root=None):
        self.root = root
        # 1. Convert existing class constructor arguments to Mutable objects
        converted_list = self._convert_iterable(source)
        super().__init__(root, converted_list)
    
    # 2. Classes with mutable items must have a _tracked_items attribute
    # _tracked_items is a list of potentially mutable items
    @property
    def _tracked_items(self):
        return list(self)
    
    # 3. Call self._changed() to register change with the root Mutable object
    def append(self, item):
        self._changed()
        super().append(self._convert(item, self.root))
        
x = MyModel()
x.mutable.nested_list = []
session.commit()
x.mutable.nested_list.append('hello world')
session.commit()
print(x.mutable.nested_list[0])
```

Outputs:

```
hello world
```

Fortunately, I have already defined ```MutableList``` and ```MutableDict``` for you. These classes underlie the functionality in Example 2.

## License

This project is licensed under the MIT License [LICENSE](LICENSE).

## Acknowledgements

Much inspiration drawn from [SQLAlchemy-JSON](https://pypi.org/project/sqlalchemy-json/)