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

1. Import classes from sqlalchemy_mutable

```python
from sqlalchemy_mutable import Mutable, MutableType, Query
```

2. Initialize a database column with ```MutableType``` (or ```MutableListType``` or ```MutableDictType```)

```python
class MyModel(Base):
    __tablename__ = 'mymodel'
    id = Column(Integer, primary_key=True)
    
    # Initialize with MutableType
    mutable = Column(MutableType)
    # ...
```

3. Add a ```query``` class attribute initialized with a [```scoped_session```](https://docs.sqlalchemy.org/en/13/orm/contextual.html#sqlalchemy.orm.scoping.scoped_session) object (skip this step if using with [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)

```python
class MyModel(Base):
    # ...
    query = Query(Session) 
    # ...
```

4. Set ```mutable``` column to ```Mutable``` object

```python
class MyModel(Base):
    # ...
    def __init__(self):
        self.mutable = Mutable()
```

## Examples

See ### link to file on github

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

### Example 5: Convert existing classes to mutable classes

Users can add mutation tracking to existing classes.

**Notes:**
1. Existing classes must be registered using ```@Mutable.register_tracked_type(<existing class>)```.
2. ```__init__``` must be defined to take a ```source``` argument (an instance of the existing class) and a ```root``` argument (the ```Mutable``` object at the root of the nested mutable objects). It begins by setting the root attribute and then calls ```super().__init__(root, *args, **kwargs)``` where ```*args``` and ```**kwargs``` are passed to constructor of the existing class.
3. If the existing class has mutable items, the new mutable class must have an attribute ```_tracked_items``` which returns a list of items.
4. Any methods of the existing class which modify the object and *do not* call ```___setattr___``` or ```__getattr__``` must be redefined to begin by calling ```self._changed()```. This registers the change with the root mutable object.

```python
# 1. Register existing type
@Mutable.register_tracked_type(list) 
class MutableList(Mutable, list):
    # 2. Define __init__
    def __init__(self, source=(), root=None):
        self.root = root
        super().__init__(root, self._convert_iterable(source))
    
    # 3. _tracked_items attribute
    @property
    def _tracked_items(self):
        return list(self)
    
    # 4. Call self._changed() to register change with the root Mutable object
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