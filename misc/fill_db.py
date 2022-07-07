from app import db, City
import requests
import json
from api_keys import OPEN_WEATHER_KEY

# this program drops the db, fills with cities from the list of all cities and calls on
# the OpenWeather API to get coordinates for each city
# Only used once because of time consuming and limited amount of calls to external API

f = open('cities.json')
cities = json.load(f)
uniqueCities = { each['Beteckning'] : each for each in cities }.values()

db.drop_all()
db.create_all()

for city in uniqueCities:
    newCity = City(name=city['Beteckning'])
    db.session.add(newCity)

db.session.commit()


for city in City.query.all():
    data = requests.get('http://api.openweathermap.org/geo/1.0/direct?q=' + city.name + ',SE&limit=1&appid='+OPEN_WEATHER_KEY).json()
    if (len(data) == 0):
        City.query.filter_by(id=city.id).delete()
        db.session.commit()
    else:
        city.longitude = data[0]['lon']
        city.latitude = data[0]['lat']
        db.session.commit()