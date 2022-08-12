from base import db
from city import City
import json
from app import app

def compare_cities(x, y):
    if x['name'] < y['name']:
        return -1
    elif x['name'] > y['name']:
        return 1
    else:
        return 0

# imports city data from json-file to db, including names and coordinates
def fill_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

        f = open('cities.json')
        cities = json.load(f)
        unique_cities = { each['name'] : each for each in cities }.values()
        from functools import cmp_to_key
        sorted_cities = sorted(unique_cities, key=cmp_to_key(compare_cities))

        for city in sorted_cities:
            db.session.add(City(name=city['name'], longitude=city['longitude'], latitude=city['latitude']))
            db.session.commit()

fill_db()