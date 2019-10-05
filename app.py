"""Flask shell with application factory structure"""

# 1. Import classes from sqlalchemy_mutable
from sqlalchemy_mutable import Mutable, MutableType, MutableModelBase

# 2. Standard app creation
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

# 3. Subclass MutableModelBase when creating database models
class MyModel(MutableModelBase, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    greeting = db.Column(db.String)
    
    # 4. Initialize a database column with MutableType
    mutable = db.Column(MutableType)  
    
    def __init__(self):
        # 6. Set mutable column to Mutable object
        self.mutable = Mutable()

app = create_app()

@app.shell_context_processor
def make_shell_context():
    # 7. Create the database
    db.create_all()
    return globals()