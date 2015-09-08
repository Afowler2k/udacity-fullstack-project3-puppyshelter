import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.ext.hybrid import hybrid_property

 
Base = declarative_base()
 
class Shelter(Base):
    __tablename__ = 'shelter'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    address = Column(String(250), nullable=False)
    city = Column(String(250), nullable=False)
    state = Column(String(250), nullable=False)
    zipCode = Column(String(250), nullable=False)
    email = Column(String(250))
    website = Column(String, nullable=False)
    _maximum_capacity = Column(Integer, nullable=False)
    _current_occupancy = Column(Integer, default=0)
    puppies = relationship("Puppy", secondary='puppy_shelter_link')

    @hybrid_property
    def maximum_capacity(self):
        return self._maximum_capacity

    @maximum_capacity.setter
    def maximum_capacity(self, value):
        self._maximum_capacity = value

    @hybrid_property 
    def current_occupancy(self):
        return self._current_occupancy

    @current_occupancy.setter
    def current_occupancy(self, value):
        self._current_occupancy = value


 
 
class Puppy(Base):
    __tablename__ = 'puppy'

    id = Column(Integer, primary_key=True)
    name =Column(String(250), nullable = False)
    dateOfBirth=Column(Date, nullable=False)
    breed=Column(String(250))
    gender=Column(String(250), nullable=False)
    weight=Column(Integer, nullable=False)
    picture=Column(String, nullable=False)
    shelter_id = Column(Integer,ForeignKey('shelter.id'))
    #shelter = relationship(Shelter) 
    profile_id = Column(Integer, ForeignKey('puppyprofile.id'))
    adopters = relationship('Adopter', secondary='puppy_adopter_link')
 
class PuppyProfile(Base):
    __tablename__ = 'puppyprofile'
    id = Column(Integer, primary_key=True)
    photo = Column(String)
    description = Column(String)
    specialNeeds = Column(String)

class Adopter(Base):
    __tablename__ = 'adopter'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    puppies = relationship('Puppy', secondary='puppy_adopter_link')

class PuppyAdopterLink(Base):
    __tablename__ = 'puppy_adopter_link'
    puppy_id = Column(Integer, ForeignKey('puppy.id'), primary_key=True)
    adopter_id = Column(Integer, ForeignKey('adopter.id'), primary_key=True)

class PuppyShelterLink(Base):
    __tablename__ = 'puppy_shelter_link'
    puppy_id = Column(Integer, ForeignKey('puppy.id'), primary_key=True)
    shelter_id = Column(Integer, ForeignKey('shelter.id'), primary_key=True)

engine = create_engine('sqlite:///puppies.db')
Base.metadata.create_all(engine)