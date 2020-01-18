"""Model Shell and Query classes

For storing (shelling) and recovering (unshelling) database models
in Mutable objects and MutableType database types
"""

from sqlalchemy import orm
from sqlalchemy.inspection import inspect


class Query():
    """Query attribute in database model"""
    def __init__(self, scoped_session):
        self.scoped_session = scoped_session
    
    def __get__(self, obj, type):
        """Return orm.Query object for use with model_class.get()"""
        return orm.Query(type, self.scoped_session())


class ModelShell():
    def __init__(self, model):
        """Store model id (primary key) and class"""
        self.id = inspect(model).identity[0]
        self.model_class = model.__class__
        
    def unshell(self):
        """Recover model"""
        if hasattr(self.model_class, 'query'):
            return self.model_class.query.get(self.id)
        return (self.model_class, self.id)
    
    def __eq__(self, obj):
        return self.unshell() == obj