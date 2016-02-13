import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class EasyRepr(object):
    def __repr__(self):
        properties = sorted(vars(self).items())
        ctor_str = ', '.join('%s=%r' % pair for pair in properties if not pair[0].startswith('_'))
        return "%s(%s)" % (self.__class__.__name__, ctor_str)


class Ping(Base, EasyRepr):
    __tablename__ = 'pings'
    date = Column(DateTime, primary_key=True)
    latency = Column(Integer, nullable=True)
    error = Column(String, nullable=True)

def open_db(host):
    fname = host + '.sqlite'
    engine = create_engine('sqlite:///' + fname)#, echo=True)
    Base.metadata.create_all(engine)
    make_session = sessionmaker(bind=engine)
    return make_session()

