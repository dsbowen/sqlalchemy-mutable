"""Setup and examples with sqlalchemy-mutable"""

"""Setup"""

# 1. Import classes from sqlalchemy_mutable
from sqlalchemy_mutable import Mutable, MutableType, MutableModelBase

# 2. Standard db.session creation
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 3. Subclass MutableModelBase when creating database models
class MyModel(db.Model, MutableModelBase):
    id = db.Column(db.Integer, primary_key=True)
    greeting = db.Column(db.String)
    
    # 4. Initialize a database column with MutableType
    mutable = db.Column(MutableType)  
    
    def __init__(self):
        # 6. Set mutable column to Mutable object
        self.mutable = Mutable()

# 7. Create the database
db.create_all()

"""Examples"""

# Example 1: Nested mutation tracking
print('Example 1: Nested mutation tracking')

x = MyModel()
db.session.add(x)
x.mutable.nested_mutable = Mutable()
db.session.commit()
x.mutable.nested_mutable.greeting = 'hello world'
db.session.commit()
print(x.mutable.nested_mutable.greeting)

# Example 2: Mutation tracking for iterables
print('\nExample 2: Mutation tracking for iterables')

x = MyModel()
db.session.add(x)
x.mutable = {'greeting': []}
db.session.commit()
x.mutable['greeting'].append('hello world')
db.session.commit()
print(x.mutable['greeting'][0])

# Example 3: Embedded database models
print('\nExample 3: Embedded database models')

x = MyModel()
y = MyModel()
db.session.add_all([x,y])
db.session.flush([x,y]) #Flush or commit models before embedding
x.mutable.y = y
db.session.commit()
y.greeting = 'hello world'
print(x.mutable.y.greeting)
print('Successfully recovered y?', x.mutable.y == y)

# Example 4: Set Mutable Columns to common literals and database models
print('\nExample 4: Set Mutable Columns to literals and database models')

x = MyModel()
y = MyModel()
db.session.add_all([x,y])
db.session.flush([x,y])
x.mutable = 'hello world'
print(x.mutable)
x.mutable = 123
print(x.mutable)
x.mutable = y
db.session.commit()
y.greeting = 'hello moon'
print(x.mutable)
print(x.mutable.greeting)
print('Successfully recovered y?', x.mutable == y)

# Example 5: Custom Mutable classes
print('\nExample 5: Custom Mutable classes')

class CustomMutable(Mutable):
    def __init__(self, name='world'):
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

# Example 6.1: Convert existing classes to mutable classes (basic use)
print('\nExample 6.1: Convert existinc classes to mutable classes (basic)')

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
db.session.add(x)
x.mutable = ExistingClass('')
x.mutable.nested_mutable = ExistingClass('world')
db.session.commit()
print(x.mutable.nested_mutable.greeting())
x.mutable.nested_mutable.name = 'moon'
db.session.commit()
print(x.mutable.nested_mutable.greeting())

# Example 6.2: Convert existing classes to mutable classes (advanced use)
print('\nExample 6.2: Convert existinc classes to mutable classes (advanced)')

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
