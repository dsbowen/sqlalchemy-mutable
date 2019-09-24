"""Setup and examples with sqlalchemy-mutable"""

"""Setup"""

# 1. Import classes from sqlalchemy_mutable
from sqlalchemy_mutable import Mutable, MutableType, Query

# 2. Standard session creation
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
    
    # 3. Initialize a database column with MutableType
    mutable = Column(MutableType) 
    # 4. Add a query class attribute initialized with a scoped_session
    query = Query(Session) 
    
    def __init__(self):
        # 5. Set mutable column to Mutable object
        self.mutable = Mutable()

# 6. Create the database
Base.metadata.create_all(engine)

"""Examples"""

# Example 1: Nested mutation tracking
x = MyModel()
session.add(x)
x.mutable.nested_mutable = Mutable()
session.commit()
x.mutable.nested_mutable.greeting = 'hello world'
session.commit()
print(x.mutable.nested_mutable.greeting)

# Example 2: Mutation tracking for iterables
x = MyModel()
session.add(x)
x.mutable = {'greeting': []}
session.commit()
x.mutable['greeting'].append('hello world')
session.commit()
print(x.mutable['greeting'][0])

# Example 3: Embedded database models
x = MyModel()
y = MyModel()
session.add_all([x,y])
session.flush([x,y]) #Flush or commit models before embedding
x.mutable.y = y
session.commit()
y.greeting = 'hello world'
print(x.mutable.y.greeting)
print('Successfully recovered y?', x.mutable.y == y)

# Example 4: ```Mutable``` base for customized mutable classes
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

# Example 5.1: Convert existing classes to mutable classes (basic use)
class ExistingClass():
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, name):
        self.name = name
    
    def greeting(self):
        return 'hello {}'.format(self.name)

# 1. Create new mutable class which inherits from Mutable and ExistingClass
# 2. Registration
@Mutable.register_tracked_type(ExistingClass)
class MutableClass(Mutable, ExistingClass):
    # 3. Initialization
    def __init__(self, source=None, root=None):
        src_name = source.name if hasattr(source, 'name') else None
        super().__init__(name=src_name)
    
    """
    For custom Mutable classes, MutableClass's __new__ method will be called 
    before construction with the instance of the ExistingClass passed as the 
    source.
    
    If the __new__ method of the ExistingClass does not accept arguments, 
    you must define a __new__ method in the MutableClass which does. 
    
    Try this first:
    
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    """
        
x = MyModel()
session.add(x)
x.mutable = ExistingClass('world')
x.mutable.nested_mutable = ExistingClass('world')
session.commit()
print(x.mutable.nested_mutable.greeting())
x.mutable.nested_mutable.name = 'moon'
session.commit()
print(x.mutable.nested_mutable.greeting())

# Example 5.2: Convert existing classes to mutable classes (advanced use)
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
session.commit()
x.mutable.nested_list.append('hello world')
session.commit()
print(x.mutable.nested_list[0])
