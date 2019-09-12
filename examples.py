"""Setup and examples with sqlalchemy-mutable"""

"""Setup in 4 steps"""

# 1. Import classes from sqlalchemy_mutable
from sqlalchemy_mutable import Mutable, MutableType, Query

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
    # 2. Initialize a database column with MutableType
    mutable = Column(MutableType) 
    # 3. Add a query class attribute initialized with a scoped_session
    query = Query(Session) 
    
    def __init__(self):
        # 4. Set mutable column to Mutable object
        self.mutable = Mutable()


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

# Example 5: Convert existing classes to mutable classes

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