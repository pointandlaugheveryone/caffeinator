from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from config import DATABASE_URI

Base = declarative_base()

# Many-to-many association table
store_drink_association = Table(
    'store_drink', Base.metadata,
    Column('store_id', Integer, ForeignKey('Stores.id')),
    Column('drink_id', Integer, ForeignKey('Drinks.id'))
)

class Drink(Base):
    __tablename__ = 'Drinks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(500), nullable=False, unique=True)
    normal_cost = Column(Float, nullable=False)
    discount_cost = Column(Float, nullable=False)
    image_url = Column(String(200))
    is_zero = Column(Integer, default=False)
    discount = Column(Integer, default=False)

    stores = relationship('Store', secondary=store_drink_association, back_populates='drinks')


class Store(Base):
    __tablename__ = 'Stores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(500), nullable=False, unique=True)
    logo_url = Column(String(500), nullable=False)

    drinks = relationship('Drink', secondary=store_drink_association, back_populates='stores')


engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()