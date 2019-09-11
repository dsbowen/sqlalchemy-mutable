"""sqlalchemy-mutable example with flask-sqlalchemy

Instructions:
1. Import from sqlalchemy_mutable
2. Initialize a database column with Mutable type
3. Set mutable column to Mutable object
4. Flush or commit models before embedding in a Mutable object
"""

# Import from sqlalchemy_mutable
from sqlalchemy_mutable import Mutable, MutableType, Query

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class MyModel(db.Model):
    __tablename__ = 'mymodel'
    id = db.Column(db.Integer, primary_key=True)
    
    # Initialize with Mutable type
    mutable = db.Column(MutableType) 
    
    def __init__(self):
        # Set mutable column to Mutable object
        self.mutable = {}


db.create_all()
x = MyModel()
y = MyModel()
db.session.add_all([x,y])

# Flush or commit a model before embedding it in a mutable object
db.session.flush([x,y])

x.mutable['nested_list'] = [y]
db.session.commit()
print('Mutable object is', x.mutable)
print('Successfully recovered y?', x.mutable['nested_list'][0] == y)

x.mutable['nested_list'].append(Mutable())
db.session.commit()
x.mutable['nested_list'][1].y = y
db.session.commit()
print('Mutable object is', x.mutable)
print('Successfully recovered y?', x.mutable['nested_list'][1].y == y)
