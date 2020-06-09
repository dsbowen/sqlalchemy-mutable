"""# Storing models"""

from sqlalchemy import orm
from sqlalchemy.inspection import inspect


class Query():
    """
    Query attribute in database model. Models which have a `query` attribute 
    will be unshelled automatically when stored and recovered in a `Mutable` 
    object. See the [setup code](setup.md).

    Parameters
    ----------
    scoped_session : sqlalchemy.orm.scoping.scoped_session
        Current scoped session.

    Attributes
    ----------
    scoped_session : sqlalchemy.orm.scoping.scoped_session
        Set from the `scoped_session` parameter.
    """
    def __init__(self, scoped_session):
        self.scoped_session = scoped_session
    
    def __get__(self, obj, type):
        """Return orm.Query object for use with model_class.get()"""
        return orm.Query(type, self.scoped_session())


class ModelShell():
    """
    The `ModelShell` stores (shells) and recovers (unshells) database 
    models in `Mutable` objects and `MutableType` columns.

    Parameters
    ----------
    model : sqlalchemy.ext.declarative.api.Base
        Database model to store.

    Attributes
    ----------
    id : usually int or str
        Identity of the model.

    model_class : class
        Class of the stored model.

    Notes
    -----
    1. The model must have an identity before it is shelled. i.e you must add 
    it to the session and commit or flush it.
    2. Models are unshelled to make comparisons the `__eq__` comparison.

    Examples
    --------
    Make sure you have run the [setup code](setup.md).

    ```python
    from sqlalchemy_mutable.model_shell import ModelShell

    model = MyModel()
    session.add(model)
    session.commit()
    shell = ModelShell(model)
    shell.unshell()
    ```

    Out:

    ```
    <__main__.MyModel at 0x7f6bd9936c50>
    ```
    """
    def __init__(self, model):
        """Store model id (primary key) and class"""
        self.id = inspect(model).identity[0]
        self.model_class = model.__class__
        
    def unshell(self):
        """
        Recover (unshell) a model.
        
        Returns
        -------
        model or (model_class, id) :
            If the original model has a `query` attribute, the orginal model 
            is returned. Otherwise, a `(model_class, id)` tuple is returned 
            which you can use to query the database to recover the model.
        """
        if hasattr(self.model_class, 'query'):
            return self.model_class.query.get(self.id)
        return (self.model_class, self.id)
    
    def __eq__(self, obj):
        return self.unshell() == obj