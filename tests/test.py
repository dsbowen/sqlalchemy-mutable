from sqlalchemy_mutable import (
    HTMLAttrsType, Mutable, MutableType, MutableManager, MutableModelBase, 
    Query, partial
)

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

import datetime
import unittest

MSG = 'test message'

engine = create_engine('sqlite:///:memory:')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = MutableManager.session = Session()
Base = declarative_base()


class Model(MutableModelBase, Base):
    __tablename__ = 'model'
    id = Column(Integer, primary_key=True)
    msg = Column(String)
    attrs = Column(HTMLAttrsType)
    mutable = Column(MutableType)
    query = Query(Session)

Base.metadata.create_all(engine)

def foo(obj):
    return obj


class MyClass():
    def __init__(self, msg):
        self.msg = msg


@Mutable.register_tracked_type(MyClass)
class MutableClass0(MyClass, Mutable):
    def __init__(self, source=None, root=None):
        super().__init__(msg=source.msg)


class TestMutable(unittest.TestCase):
    def test_model(self):
        model1, model2 = Model(), Model()
        model1.mutable = model2
        session.add_all([model1, model2])
        session.commit()
        model2.msg = MSG
        self.assertEqual(model1.mutable.msg, model2.msg)

    def test_nested(self):
        model = Model()
        model.mutable = Mutable()
        model.mutable.mutable = Mutable()
        session.add(model)
        session.commit()
        model.mutable.mutable.msg = MSG
        session.commit()
        self.assertEqual(model.mutable.mutable.msg, MSG)

    def test_list(self):
        model = Model()
        model.mutable = [[1,2,3]]
        session.add(model)
        session.commit()
        model.mutable[0].append(4)
        session.commit()
        self.assertEqual(model.mutable[0], [1,2,3,4])

    def test_tuple(self):
        model = Model()
        model.mutable = ([1,2,3],)
        session.add(model)
        session.commit()
        model.mutable[0].append(4)
        session.commit()
        self.assertEqual(model.mutable[0], [1,2,3,4])

    def test_dict(self):
        model = Model()
        model.mutable = {'key': [1,2,3]}
        session.add(model)
        session.commit()
        model.mutable['key'].append(4)
        session.commit()
        self.assertEqual(model.mutable['key'], [1,2,3,4])

    def test_partial(self):
        model0, model1 = Model(), Model()
        model0.mutable = partial(foo, model1)
        session.add_all([model0, model1])
        self.assertEqual(model0.mutable(), model1)

    def test_coerced_types(self):
        model = Model()
        model.mutable = True
        model.mutable = complex(1, 1)
        model.mutable = 1.
        model.mutable = 1
        model.mutable = 'hello world'
        model.mutable = datetime.datetime.now()
        model.mutable = foo

    def test_custom_tracked_type(self):
        model = Model()
        model.mutable = Mutable()
        model.mutable.object = MyClass('Some message')
        session.add(model)
        session.commit()
        model.mutable.object.msg = MSG
        session.commit()
        self.assertEqual(model.mutable.object.msg, MSG)

    def test_html_attrs(self):
        model = Model()
        model.attrs = {
            'class': ['class0'], 
            'style': {'width': '25px'},
            'disabled': True
        }
        session.add(model)
        session.commit()
        model.attrs['class'].append('class1')
        session.commit()
        self.assertEqual(
            model.attrs.to_html(), 
            'class="class0 class1" style="width:25px;" disabled'
        )