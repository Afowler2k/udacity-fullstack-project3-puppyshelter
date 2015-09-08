from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import asc
from sqlalchemy.sql.expression import desc
 
from shelter_setup import Base, Shelter, Puppy
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random


engine = create_engine('sqlite:///puppies.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

# query all puppies return in ascending alphabetical order
for puppy in session.query(Puppy).order_by(asc(Puppy.name)):
	print puppy.name

#query all puppied that are less than 6 months old organized by the youngest first
for puppy in session.query(Puppy).\
				filter(Puppy.dateOfBirth > datetime.date.today() - datetime.timedelta(weeks = 24)).\
				order_by(desc(Puppy.dateOfBirth)):
	print puppy.name, puppy.dateOfBirth

#query all puppies by ascending weight
for puppy in session.query(Puppy).order_by(asc(Puppy.weight)):
	print puppy.name, puppy.weight

#query all puppies grouped by the shelter in which they are staying
for puppy, shelter in session.query(Puppy, Shelter).\
				filter(Puppy.shelter_id==Shelter.id).\
				order_by(Shelter.name):
	print puppy.name, puppy.id, shelter.name, shelter.id
