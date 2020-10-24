"""# Mutable manager"""

class MutableManager():
    """
    Ordinarily, if you want to store a database model in a mutable object, you
    need to make sure the model has an identity by adding then 
    flushing/committing to the database.

    The mutable manager takes care of this for you. If using SQLAlchemy, set
    the `session` attribute to your session. If using Flask-SQLAlchemy, set
    the `db` attribute to your database (`flask_sqlalchemy.SQLAlchemy`).

    Examples
    --------
    Run this after the SQLAlchemy setup.

    ```python
    from sqlalchemy_mutable import MutableManager

    # for sqlalchemy
    MutableManager.session = session
    # for flask-sqlalchemy
    MutableManager.db = db
    ```

    Then you can store models in mutable columns without adding and 
    flushing/committing.

    ```python
    model0 = MyModel()
    model1 = MyModel()
    model0.mutable = model1
    ```
    """
    # Flask-SQLAlchemy database
    db = None
    # SQLAlchemy session
    session = None