"""Setup and examples with sqlalchemy-mutable"""

"""Setup"""

# 1. Import classes from sqlalchemy_mutable
from sqlalchemy_mutable import Mutable, MutableType

# 2. Standard session creation
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class MyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    greeting = db.Column(db.String)
    
    # 3. Initialize a database column with MutableType
    mutable = db.Column(MutableType)  
    
    def __init__(self):
        # 5. Set mutable column to Mutable object
        self.mutable = Mutable()


db.create_all()

"""Examples"""

# Example 1: Nested mutation tracking
x = MyModel()
db.session.add(x)
x.mutable.nested_mutable = Mutable()
db.session.commit()
x.mutable.nested_mutable.greeting = 'hello world'
db.session.commit()
print(x.mutable.nested_mutable.greeting)

# Example 2: Mutation tracking for iterables
x = MyModel()
db.session.add(x)
x.mutable = {'greeting': []}
db.session.commit()
x.mutable['greeting'].append('hello world')
db.session.commit()
print(x.mutable['greeting'][0])

# Example 3: Embedded database models
x = MyModel()
y = MyModel()
db.session.add_all([x,y])
db.session.flush([x,y]) #Flush or commit models before embedding
x.mutable.y = y
db.session.commit()
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
db.session.add(x)
x.mutable.nested_mutable = CustomMutable()
db.session.commit()
print(x.mutable.nested_mutable.greeting())
x.mutable.nested_mutable.name = 'moon'
db.session.commit()
print(x.mutable.nested_mutable.greeting())

# Example 5.1: Convert existing classes to mutable classes (basic use)
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
db.session.add(x)
x.mutable.nested_mutable = ExistingClass('world')
db.session.commit()
print(x.mutable.nested_mutable.greeting())
x.mutable.nested_mutable.name = 'moon'
db.session.commit()
print(x.mutable.nested_mutable.greeting())

# Example 5.2: Convert existing classes to mutable classes (advanced use)
@Mutable.register_tracked_type(list) 
class MutableList(Mutable, list):
    def __init__(self, source=(), root=None):
        self.root = root
        # 1. Convert existing class method arguments to Mutable objects
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
db.session.commit()
x.mutable.nested_list.append('hello world')
db.session.commit()
print(x.mutable.nested_list[0])