from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from config import DATABASE_URI

Base = declarative_base()

class Store(Base):
    __tablename__ = 'Stores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(500), nullable=False, unique=True)
    logo_url = Column(String(500), nullable=False)


class Drink(Base):
    __tablename__ = 'Drinks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(500), nullable=False, unique=True)
    normal_cost = Column(Float, nullable=False)
    discount_cost = Column(Float, nullable=False)
    image_url = Column(String(200))
    is_zero = Column(Integer, default=False)
    discount = Column(Integer, default=False)

    store_id = Column(Integer, ForeignKey('Stores.id'))
    store = relationship('Store')


engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()