
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
    mutable = Column(MutableType)
    
    query = Query(Session)
    
    def __init__(self):
        self.mutable = Mutable()


Base.metadata.create_all(engine)
x = MyModel()
y = MyModel()
session.add_all([x,y])
session.flush([x,y])

x.mutable.y = y
session.commit()
print(x.mutable)
print(x.mutable.y)
print('Successfully recovered y?', x.mutable.y == y)

x.mutable.mutable = Mutable()
x.mutable.mutable.y = y
session.commit()
print(x.mutable)
print(x.mutable.mutable.y)
print('Successfully recovered y?', x.mutable.mutable.y == y)
