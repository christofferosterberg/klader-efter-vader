from base import db
from city import City
import json
from app import app

# imports city data from json-file to db, including names and coordinates
with app.app_context():
    db.drop_all()
    db.create_all()

    f = open('cities.json')
    cities = json.load(f)
    uniqueCities = { each['name'] : each for each in cities }.values()

    for city in uniqueCities:
        db.session.add(City(name=city['name'], longitude=city['longitude'], latitude=city['latitude']))
        db.session.commit()
