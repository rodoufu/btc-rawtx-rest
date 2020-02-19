from datetime import datetime
from flask import abort


def get_timestamp():
	return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


PEOPLE = {}


def add_to_people(person):
	PEOPLE[person["lname"]] = {
		"lname": person["lname"],
		"fname": person["lname"],
		"timestamp": get_timestamp(),
	}


add_to_people({
	"fname": "Doug",
	"lname": "Farrell",
	"timestamp": get_timestamp()
})
add_to_people({
	"fname": "Kent",
	"lname": "Brockman",
	"timestamp": get_timestamp()
})
add_to_people({
	"fname": "Bunny",
	"lname": "Easter",
	"timestamp": get_timestamp()
})


def read_all():
	"""
	This function responds to a request for /api/people
	with the complete lists of people

	:return: sorted list of people
	"""
	return [PEOPLE[key] for key in sorted(PEOPLE.keys())]


def read_one(lname):
	"""
	This function responds to a request for /api/people/{lname}
	with one matching person from people
	:param lname:   last name of person to find
	:return: person matching last name
	"""
	if lname in PEOPLE:
		return PEOPLE[lname]
	else:
		abort(404, f"Person with last name {lname} not found")


def create(person):
	"""
	This function creates a new person in the people structure
	based on the passed in person data
	:param person:  person to create in people structure
	:return:        201 on success, 406 on person exists
	"""
	lname = person["lname"]

	if lname not in PEOPLE and lname is not None:
		add_to_people(person)
		return {"msg": f"{lname} successfully created"}, 201
	else:
		abort(406, f"Person with the last name {lname} already exists")


def update(lname, person):
	"""
	This function updates an existing person in the people structure
	:param lname:   last name of person to update in the people structure
	:param person:  person to update
	:return:        updated person structure
	"""
	if lname in PEOPLE:
		add_to_people(person)
	else:
		abort(404, f"Person with last name {lname} not found")


def delete(lname):
	"""
	This function deletes a person from the people structure
	:param lname:   last name of person to delete
	:return:        200 on successful delete, 404 if not found
	"""
	if lname in PEOPLE:
		del PEOPLE[lname]
		return {"msg": f"{lname} successfully deleted"}, 200
	else:
		abort(404, f"Person with last name {lname} not found")
