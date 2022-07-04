from base import db
from sqlalchemy import ForeignKey
import requests
from datetime import datetime
from city import City

class Weather(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    hour          = db.Column(db.Integer, nullable=False)
    day           = db.Column(db.Integer, nullable=False)
    month         = db.Column(db.Integer, nullable=False)
    year          = db.Column(db.Integer, nullable=False)
    fetched       = db.Column(db.DateTime, nullable=False)
    description   = db.Column(db.Text(30), nullable=False)
    value         = db.Column(db.Integer, nullable=False)
    temperature   = db.Column(db.Float, nullable=False)
    cloudiness    = db.Column(db.Integer, nullable=False)
    precipitation = db.Column(db.Float, nullable=False)
    wind_speed     = db.Column(db.Float, nullable=False)

    city_id       = db.Column(db.Integer, ForeignKey('city.id'))
    city_name     = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Weather {}: {} {} {} {} {} {} {} {} {} {} {} {} {}>'.format(self.id, self.hour, self.day, self.month, self.year, 
        self.fetched, self.description, self.value, self.temperature, self.cloudiness, self.precipitation, self.wind_speed, self.city_id, self.city_name)

    def serialize(self):
        return dict(id=self.id, hour=self.hour, day=self.day, month=self.month, year=self.year, 
        fetched = self.fetched, description=self.description, value=self.value, temperature=self.temperature, 
        cloudiness = self.cloudiness, precipitation = self.precipitation, wind_speed=self.wind_speed, city_id=self.city_id, city_name=self.city_name)


def translate_weather_description(value):
    weather_info = {
        1: 'Inte ett moln i sikte!',
        2: 'Enstaka moln kan dyka upp',
        3: 'Moln kommer och går',
        4: 'Halvklart, moln finns absolut',
        5: 'Väldigt mycket moln :(',
        6: 'Ingen sol öht :(',
        7: 'Dimma, kör försiktigt!',
        8: 'Några få regnskurar kan förekomma',
        9: 'Det kommer bli regnskurar',
        10: 'Ösregn-skurar',
        11: 'Åskstorm!',
        12: 'En gnutta slaskskurar',
        13: 'Slaskskurar',
        14: 'En massa slaskskurar',
        15: 'Några få snöskurar kan förekomma',
        16: 'Lagom många snöskurar',
        17: 'Massa snöskurar',
        18: 'Lite duggregn',
        19: 'Lagom mycket regn',
        20: 'Ösregn',
        21: 'Tor kommer med hammaren (åska)',
        22: 'En gnutta slaskregn',
        23: 'Lagom mycket slaskregn',
        24: 'En massa slaskregn',
        25: 'Några få söflingor kommer synas, fint!',
        26: 'Lagom mycket snö',
        27: 'Snöstorm!'
    }
    return weather_info[value]

def fetch_weather(city):
    lon = int(round(city.longitude, 0))
    lat = int(round(city.latitude, 0))
    data = requests.get('https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/'+str(lon)+'/lat/'+str(lat)+'/data.json').json()
    time_series = data['timeSeries']
    
    for time_serie in time_series:
        year = time_serie['validTime'][0:4]
        month = time_serie['validTime'][5:7]
        day = time_serie['validTime'][8:10]
        hour = time_serie['validTime'][11:13]

        parameters  = time_serie['parameters']
        description = translate_weather_description(int(parameters[18]['values'][0]))
        for parameter in parameters:
            if parameter['name'] == 't':
                temperature = parameter['values'][0]
            elif parameter['name'] == 'Wsymb2':
                value = int(parameter['values'][0])
            elif parameter['name'] == 'tcc_mean':
                cloudiness  = parameter['values'][0]
            elif parameter['name'] == 'pmean':
                precipitation = parameter['values'][0]
            elif parameter['name'] == 'ws':
                wind_speed = parameter['values'][0]
        newWeather = Weather(hour = hour, day = day, month = month, year = year, fetched = datetime.now(), description=description, 
        value=value, temperature=temperature, cloudiness=cloudiness, precipitation=precipitation, wind_speed=wind_speed, 
        city_id=city.id, city_name=city.name)
        db.session.add(newWeather)
        db.session.commit()

def up_to_date(weather):
    if datetime.now().day != weather.fetched.day:
        return False
    elif datetime.now().hour - weather.fetched.hour > 4:
        return False
    else:
        return True

def update_weather(city):
    weathers = Weather.query.filter_by(city_id = city.id)
    for weather in weathers:
        db.session.delete(weather)
        db.session.commit()
    fetch_weather(City.query.filter_by(id = city.id).first())

def get_latest_weather(city):
    last_hour = datetime.now().hour
    today = datetime.now()
    weather = Weather.query.filter_by(city_id = city.id,
                                      hour    = last_hour,
                                      day     = today.day,
                                      month   = today.month,
                                      year    = today.year).first()
    if weather == None:
        fetch_weather(city)
        weather = Weather.query.filter_by(city_id = city.id,
                                      hour    = last_hour,
                                      day     = today.day,
                                      month   = today.month,
                                      year    = today.year).first()
    elif not up_to_date(weather):
        update_weather(city)
        weather = Weather.query.filter_by(city_id = city.id,
                                      hour    = last_hour,
                                      day     = today.day,
                                      month   = today.month,
                                      year    = today.year).first()
    return weather


def get_todays_weather(city):
    today = datetime.now()
    weather = Weather.query.filter_by(city_id = city.id,
                                      day     = today.day,
                                      month   = today.month,
                                      year    = today.year).all()
    if len(weather) == 0:
        fetch_weather(city)
        weather = Weather.query.filter_by(city_id = city.id,
                                      day     = today.day,
                                      month   = today.month,
                                      year    = today.year).all()
    elif not up_to_date(weather[0]):
        update_weather(city)
        weather = Weather.query.filter_by(city_id = city.id,
                                      day     = today.day,
                                      month   = today.month,
                                      year    = today.year).all()
    return weather