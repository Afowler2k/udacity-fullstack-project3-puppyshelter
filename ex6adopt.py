from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import asc
from sqlalchemy.sql.expression import desc
 
from shelter_setup import Base, Shelter, Puppy, Adopter
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random


def AdoptPuppy(session, puppy_id, adopters):

	query = session.query(Puppy).filter(Puppy.id == puppy_id)
	puppy = query.first()
	if puppy is None:
		print ("This is not a puppy in our system!")
		return

	print puppy.name, puppy.shelter_id

	query = session.query(Shelter).filter(Shelter.id == puppy.shelter_id)
	shelter = query.first()
	if shelter is None:
		print("This puppy has not been sheltered!")
		return

	shelter.puppies.remove(puppy)
	shelter.current_occupancy = shelter.current_occupancy - 1

	for adopter in adopters:		
		puppy.adopters.append(adopter)

	session.commit()



engine = create_engine('sqlite:///puppies.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

# create a new puppy
new_adopter = Adopter(name = "Andy")
session.add(new_adopter)

AdoptPuppy(session, 106, [new_adopter])
