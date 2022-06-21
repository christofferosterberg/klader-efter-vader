from datetime import datetime
from flask import Flask, request, jsonify, render_template
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, delete
from sqlalchemy.orm import relationship
import pytz

app = Flask(__name__, static_folder='client', static_url_path='/')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'U0A6DRhYvG3XXgzWCUEGvu5F9UuvVCAiSYwicGbKIFpktoSb5WSgf7Fkp_YbAXhQ'
db = SQLAlchemy(app)

timezone = pytz.timezone('Europe/Stockholm')

host = 'http://localhost:3000'


# Classes in db
class City(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(50), unique=True, nullable=False)
    longitude = db.Column(db.Float, nullable=True)
    latitude  = db.Column(db.Float, nullable=True)
    weathers  = relationship('Weather')

    def __repr__(self):
        return '<City {}: {} {} {}>'.format(self.id, self.name, self.longitude, self.latitude)

    def serialize(self):
        return dict(id=self.id, name=self.name, longitude=self.longitude, latitude=self.latitude)

class Weather(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    datetime    = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text(30), nullable=False)
    value       = db.Column(db.Integer, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    windSpeed   = db.Column(db.Float, nullable=False)

    city_id     = db.Column(db.Integer, ForeignKey('city.id'))
    city_name   = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Weather {}: {} {} {} {} {} {} {}>'.format(self.id, self.datetime, self.description, self.value, self.temperature, self.windSpeed, self.city_id, self.city_name)

    def serialize(self):
        return dict(id=self.id, datetime=self.datetime, description=self.description, value=self.value, temperature=self.temperature, windSpeed=self.windSpeed, city_id=self.city_id, city_name=self.city_name)
    




#Gets a datetime in string format "YYYY-MM-DD HH:MM:SS"
def str_datetime(datetime_string):
    if datetime_string is None:
        return datetime_string
    if isinstance(datetime_string, datetime):
        return datetime_string
    date_time = timezone.localize(datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S'))
    return date_time

def translateWeatherDescription(value):
    weatherInfo = {
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
    return weatherInfo[value]

def getWeatherData():
    Weather.__table__.drop(db.engine)
    Weather.__table__.create(db.engine)
    cities = []
    cities.append(City.query.filter_by(name='Stockholm').first())
    cities.append(City.query.filter_by(name='Göteborg').first())
    cities.append(City.query.filter_by(name='Malmö').first())

    for city in cities:
        lon = int(round(city.longitude, 0))
        lat = int(round(city.latitude, 0))
        data = requests.get('https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/'+str(lon)+'/lat/'+str(lat)+'/data.json').json()
        timeSeries = data['timeSeries']
    
        for timeSerie in timeSeries:
            date = timeSerie['validTime'][0:10]
            time = timeSerie['validTime'][11:19]
            dt = str(date) + ' ' + str(time)

            parameters  = timeSerie['parameters']
            description = translateWeatherDescription(int(parameters[18]['values'][0]))
            value       = int(parameters[18]['values'][0])
            temperature = parameters[1]['values'][0]
            windSpeed   = parameters[4]['values'][0]

            newWeather = Weather(datetime=str_datetime(dt), description=description, value=value, temperature=temperature, windSpeed=windSpeed, city_id=city.id, city_name=city.name)
            db.session.add(newWeather)
    
    db.session.commit()



@app.route('/')
def client():
    # getWeatherData()
    return app.send_static_file('client.html')

def getLatestWeather(city_id):
    return Weather.query.filter_by(city_id = city_id).first()

@app.route('/weather', methods=['GET'])
def weather():
    if request.method == 'GET':
        cities = City.query.all()
        weatherData = []
        for city in cities:
            weather = getLatestWeather(city.id)
            weatherData.append(weather.serialize())
        return jsonify(weatherData)

@app.route('/clothes-info/<city_name>', methods=['GET'])
def getClothesChoice(city_name):
    city = City.query.filter_by(name=city_name).first()
    weatherData = Weather.query.filter_by(city_id = city.id).all()
    weather1 = weatherData[1]
    weather2 = weatherData[7]
    clothes = getClothes(weather1, weather2)
    return jsonify(clothes)

@app.route('/city-names', methods=['GET'])
def getCityNames(city_name):
    cities = []
    for city in City.query.all():
        cities.append(city)
    return jsonify(cities)

def getClothes(weather1, weather2):
    clothesOptions = {
        1: 'en skön t-shirt och ett par shorts eller kjol. Glöm inte solkrämen!', #strålande sol och varmt
        2: 'ett par långbyxor och en längre tröja eller jacka, det ska inte bli jättevarmt trots solen.',
        3: 'en tjocktröja och eventuellt även en jacka. Det är kallt idag.',
        4: 'regnkläder kommer behövas!'
    }
    clothesCategory1 = getClothesCategory(weather1.value, weather1.temperature)
    clothesCategory2 = getClothesCategory(weather2.value, weather2.temperature)

    if (clothesCategory1 == clothesCategory2):
        return 'Ta på dig ' + clothesOptions[clothesCategory1]
    else:
        return 'Ta på dig ' + clothesOptions[clothesCategory1] + ' Ta även med dig ' + clothesOptions[clothesCategory2]


def getClothesCategory(value, temperature):
    weatherCategory = 0
    if (value > 0 and value < 4):
        weatherCategory = 1
    elif ((value > 4 and value < 9) or value == 18):
        weatherCategory = 2
    elif ((value > 8 and value < 18) or value > 18):
        weatherCategory = 3
    
    if (weatherCategory == 1 and temperature > 20):
        return 1
    elif (weatherCategory == 1):
        return 2
    elif (weatherCategory == 2 and temperature > 20):
        return 2
    elif (weatherCategory == 2):
        return 3
    elif (weatherCategory == 3 and temperature > 20):
        return 4
    else:
        return 5
    


if __name__ == '__main__':
    app.run(debug=True, port=3000)