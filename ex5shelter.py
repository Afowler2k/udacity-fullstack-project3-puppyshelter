from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import asc
from sqlalchemy.sql.expression import desc
 
from shelter_setup import Base, Shelter, Puppy
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random

#This method will make a random age for each puppy between 0-18 months(approx.) old from the day the algorithm was run.
def CreateRandomAge():
	today = datetime.date.today()
	days_old = randint(0,540)
	birthday = today - datetime.timedelta(days = days_old)
	return birthday

#This method will create a random weight between 1.0-40.0 pounds (or whatever unit of measure you prefer)
def CreateRandomWeight():
	return random.uniform(1.0, 40.0)


#this method will check a puppy into a shelter and increase the occupancy
def PuppyCheckIn(session, puppy):

	# ask user which shelter to check new puppy into
	shelter = None
	while shelter is None:
		shelter_id = raw_input('Enter a shelter id:')
		print shelter_id
		query = session.query(Shelter).filter(Shelter.id == shelter_id)
		shelter = query.first();
		if shelter is None:
			print("This shelter does not exist! Please try another shelter.")


	# make sure shelter can handle this puppy
	if shelter.current_occupancy == shelter.maximum_capacity:
		print("This shelter is full. Please try another shelter.")

		#look for other shelters in this zipcode with space
		query = session.query(Shelter).filter(Shelter.zipCode == shelter.zipCode).\
									   filter(Shelter.id != shelter.id).\
									   filter(Shelter.current_occupancy != Shelter.maximum_capacity)
		shelters = query.all()
		if len(shelters) == 0:
			print("There are no other shelters in this zipcode with space.")

			# look for any shelter with space
			query = session.query(Shelter).filter(Shelter.current_occupancy != Shelter.maximum_capacity).\
										   filter(Shelter.id != shelter.id)
			shelters = query.all()
			if len(shelters) == 0:
				print("There are no shelters in the system that have any vacancies. A new shelter needs to be built!")
			else:
				print("The following shelters are available outside of this area:")
				for shelter in shelters:
					print shelter.name, shelter.address, shelter.zipCode, "id=", shelter.id
		else:
			print("You can try these other shelters in the area:")
			for shelter in shelters:
				print shelter.name, shelter.address,  "id=", shelter.id

	else:
		#space available check in the puppy
		shelter.puppies.append(puppy)
		shelter.current_occupancy = shelter.current_occupancy+1
		puppy.shelter_id = shelter.id;	
		session.commit()
		print("Thank you for dropping your puppy off to the shelter")

engine = create_engine('sqlite:///puppies.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

# create a new puppy
new_puppy = Puppy(name = "Radar", gender = "male", dateOfBirth = CreateRandomAge(), weight= CreateRandomWeight(), picture="http://pixabay.com/get/da0c8c7e4aa09ba3a353/1433170694/dog-785193_1280.jpg?direct")
session.add(new_puppy)
PuppyCheckIn(session, new_puppy)


