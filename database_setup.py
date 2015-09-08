import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

 
Base = declarative_base()
 
class Shelter(Base):
    __tablename__ = 'shelter'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    address = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    city = Column(String(250), nullable=False)
    state = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
 
 
class Puppy(Base):
    __tablename__ = 'puppy'

    id = Column(Integer, primary_key=True)
    name =Column(String(250), nullable = False)
    dob=Column(Date, nullable=False)
    breed=Column(String(250), nullable=False)
    gender=Column(String(250), nullable=False)
    weight=Column(Integer, nullable=False)
    shelter_id = Column(Integer,ForeignKey('shelter.id'))
    shelter = relationship(Shelter) 
 

engine = create_engine('sqlite:///puppies.db')
Base.metadata.create_all(engine)