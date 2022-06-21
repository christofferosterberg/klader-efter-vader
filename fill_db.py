from app import db, City
import json

# imports city data from json-file to db, including names and coordinates

db.drop_all()
db.create_all()

f = open('cities.json')
cities = json.load(f)
uniqueCities = { each['name'] : each for each in cities }.values()

for city in uniqueCities:
    # name = city['name'][:-1]
    db.session.add(City(name=city['name'], longitude=city['longitude'], latitude=city['latitude']))
    db.session.commit()
