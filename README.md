# SQLAlchemy-Mutable

SQLAlchemy-Mutable provides generic nested mutable objects and iterables for [SQLAlchemy](https://www.sqlalchemy.org). Its primary features are:

1. Nested mutation tracking
2. Mutation tracking for iterables (```list``` and ```dict```)
3. Support for embedded database models
4. Support for common literals
5. Support for custom Mutable classes
6. Support for converting existing classes to Mutable classes

## License

Publications which use this software should include the following citation:

Bowen, D.S. (2019). SQLAlchemy-Mutable \[Computer software\]. [https://github.com/dsbowen/sqlalchemy-mutable](https://github.com/dsbowen/sqlalchemy-mutable)

This project is licensed under the MIT License [LICENSE](https://github.com/dsbowen/sqlalchemy-mutable/blob/master/LICENSE).

## Getting Started

### Installation

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart):

```
$ pip install -U sqlalchemy-mutable
```

### Setup

The following code will get you started with SQLAlchemy-Mutable as quickly as possible:

```python
# 1. Import classes from sqlalchemy_mutable
from sqlalchemy_mutable import Mutable, MutableType, MutableModelBase, Query

# 2. Standard session creation
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///:memory:')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()
Base = declarative_base()

# 3. Subclass MutableModelBase when creating database models
class MyModel(Base, MutableModelBase):
    __tablename__ = 'mymodel'
    id = Column(Integer, primary_key=True)
    greeting = Column(String)
    
    # 4. Initialize a database column with MutableType
    mutable = Column(MutableType) 
    # 5. Add a query class attribute initialized with a scoped_session
    query = Query(Session) 
    
    def __init__(self):
        # 6. Set mutable column to Mutable object
        self.mutable = Mutable()

# 7. Create the database
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
session.flush([x,y]) #Flush or commit models before embedding
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

### Example 4: Set Mutable Columns to common literals and database models

```MutableType``` columns can take on the values of common Python literals and even other database models.

```python
x = MyModel()
y = MyModel()
session.add_all([x,y])
session.flush([x,y])
x.mutable = 'hello world'
print(x.mutable)
x.mutable = 123
print(x.mutable)
x.mutable = y
session.commit()
y.greeting = 'hello moon'
print(x.mutable)
print(x.mutable.greeting)
print('Successfully recovered y?', x.mutable == y)
```

Outputs:

```
hello world
123
<__main__.MyModel object at 0x03924F10>
hello moon
Successfully recovered y? True
```

### Example 5: Custom Mutable classes

Users can define custom mutable classes by subclassing ```Mutable```.

```python
class CustomMutable(Mutable):
    def __init__(self, name='world'):
        self.name = name
        
    def greeting(self):
        return 'hello {}'.format(self.name)

x = MyModel()
session.add(x)
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

### Example 6.1: Convert existing classes to mutable classes (basic use)

Users can add mutation tracking to existing classes. The basic steps are:
1. Create a new mutable class which inherits from ```Mutable``` and the existing class.
2. Associate the new mutable class with the existing class using```@Mutable.register_tracked_type(<Existing Class>)```.
3. Define the new mutable class constructor. ```__init__``` takes a ```source``` (an instance of the existing class) and a ```root```, which ```Mutable``` will handle. Use ```source``` to pass arguments to the existing class constructor using ```super().__init__```.

You can now treat the existing class as if it were mutable.

```python
class ExistingClass():
    def __init__(self, name):
        self.name = name
    
    def greeting(self):
        return 'hello {}'.format(self.name)

# 1. Create new mutable class which inherits from Mutable and ExistingClass
# 2. Registration
@Mutable.register_tracked_type(ExistingClass)
class MutableClass(Mutable, ExistingClass):
    # 3. Initialization
    # source will be an instance of ExistingClass
    def __init__(self, source=None, root=None):
        super().__init__(name=source.name)
        
x = MyModel()
session.add(x)
x.mutable = ExistingClass('')
x.mutable.nested_mutable = ExistingClass('world')
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

### Example 6.2: Convert existing classes to mutable classes (advanced use)

Notes for converting more complex existing classes to mutable classes:
1. *Existing class methods take (potentially) mutable arguments*. Convert existing class method arguments to ```Mutable``` objects before passing to the existing class method with ```super().<method>(<converted arguments>)```. ```Mutable``` provides convenience methods for converting arguments:
    1. ```_convert_item(item)``` converts a single item.
    2. ```_convert_iterable(iterable)``` converts iterables like ```list```.
    3. ```_convert_mapping(mapping)``` converts key:value mappings like ```dict```.
2. *The existing class contains items other than its attributes whose mutations you want to track*. For example, a ```list``` contains potentially mutable items which are not attributes. In this case, the new mutable class must have a ```_tracked_items``` attribute which lists these items.
3. *The existing class has methods which mutate the object but do not call ```__setattr___```, ```___delattr___```, ```___setitem___```, or ```__delitem__```*. The new mutable class must redefine these methods to call ```self._changed()``` in addition to the existing class method ```super().<method>()```.

```python
@Mutable.register_tracked_type(list) 
class MutableList(Mutable, list):
    def __init__(self, source=[], root=None):
        # 1. Convert potentially mutable attributes/items to Mutable objects
        converted_list = self._convert_iterable(source)
        super().__init__(converted_list)
    
    # 2. Classes with mutable items must have a _tracked_items attribute
    # _tracked_items is a list of potentially mutable items
    @property
    def _tracked_items(self):
        return list(self)
    
    # 3. Call self._changed() to register change with the root Mutable object
    def append(self, item):
        self._changed()
        super().append(self._convert_item(item))
        
x = MyModel()
x.mutable.nested_list = []
db.session.commit()
x.mutable.nested_list.append('hello world')
db.session.commit()
print(x.mutable.nested_list[0])
```

Outputs:

```
hello world
```

Fortunately, I have already defined ```MutableList``` and ```MutableDict```. These classes underlie the functionality in Example 2.

## Acknowledgements

Much inspiration drawn from [SQLAlchemy-JSON](https://pypi.org/project/sqlalchemy-json/)