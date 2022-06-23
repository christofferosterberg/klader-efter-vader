from datetime import datetime, timedelta
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
    hour        = db.Column(db.Integer, nullable=False)
    day         = db.Column(db.Integer, nullable=False)
    month       = db.Column(db.Integer, nullable=False)
    year        = db.Column(db.Integer, nullable=False)
    fetched     = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text(30), nullable=False)
    value       = db.Column(db.Integer, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    windSpeed   = db.Column(db.Float, nullable=False)

    city_id     = db.Column(db.Integer, ForeignKey('city.id'))
    city_name   = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Weather {}: {} {} {} {} {} {} {} {} {} {} {}>'.format(self.id, self.hour, self.day, self.month, self.day, 
        self.fetched, self.description, self.value, self.temperature, self.windSpeed, self.city_id, self.city_name)

    def serialize(self):
        return dict(id=self.id, hour=self.hour, day=self.day, month=self.month, year=self.year, 
        fetched = self.fetched, description=self.description, value=self.value, temperature=self.temperature, windSpeed=self.windSpeed, city_id=self.city_id, city_name=self.city_name)
    




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

def fetchWeather(city):
    lon = int(round(city.longitude, 0))
    lat = int(round(city.latitude, 0))
    data = requests.get('https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/'+str(lon)+'/lat/'+str(lat)+'/data.json').json()
    timeSeries = data['timeSeries']
    
    for timeSerie in timeSeries:
        year = timeSerie['validTime'][0:4]
        month = timeSerie['validTime'][5:7]
        day = timeSerie['validTime'][8:10]
        hour = timeSerie['validTime'][11:13]

        parameters  = timeSerie['parameters']
        description = translateWeatherDescription(int(parameters[18]['values'][0]))
        value       = int(parameters[18]['values'][0])
        temperature = parameters[1]['values'][0]
        windSpeed   = parameters[4]['values'][0]

        newWeather = Weather(hour = hour, day = day, month = month, year = year, fetched = datetime.now(), description=description, value=value, temperature=temperature, windSpeed=windSpeed, city_id=city.id, city_name=city.name)
        db.session.add(newWeather)
        db.session.commit()

def wrongDay(date1, date2):
    if (date1.year != date2.year):
        return True
    elif (date1.month != date2.month):
        return True
    elif (date1.day != date2.day):
        return True
    else:
        return False

def upToDate(weather):
    last_hour = datetime.now().hour
    today = datetime.now()
    print('väder innan: ')
    print(weather[0])
    if weather[0].datetime.hour != last_hour or wrongDay(today, weather[0].datetime):
        Weather.__table__.delete().where(Weather.city_id == weather[0].city_id)
        fetchWeather(City.query.filter_by(id = weather[0].city_id).first())
        weather = Weather.query.filter_by(city_id = weather[0].city_id).first()
    print('väder efter')
    print(weather)
    return weather[0]

def updateWeather(weather):
    return None

def getLatestWeather(city):
    last_hour = datetime.now().hour
    today = datetime.now()
    weather = Weather.query.filter_by(city_id = city.id,
                                      hour    = last_hour,
                                      day     = today.day,
                                      month   = today.month,
                                      year    = today.year).first()
    if weather == None:
        fetchWeather(city)
        print('hämtar nytt väder för ' + city.name)
        weather = Weather.query.filter_by(city_id = city.id,
                                      hour    = last_hour,
                                      day     = today.day,
                                      month   = today.month,
                                      year    = today.year).first()
        print(weather)
    # elif not upToDate(weather):
    #     weather = updateWeather(weather)
    #     print('uppdaterar väder för ' + city.name)
    #     print(weather)
    return weather

# ROUTES

@app.route('/')
def client():
    return app.send_static_file('client.html')


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        wantedCities = request.json
        weatherData = []
        for city in wantedCities:
            theCity = City.query.filter_by(name=city).first()
            weather = getLatestWeather(theCity)
            weatherData.append(weather.serialize())
        return jsonify(weatherData)

@app.route('/clothes-info/<city_name>', methods=['GET'])
def getClothesChoice(city_name):
    city = City.query.filter_by(name=city_name).first()
    if (getLatestWeather(city) == None):
        fetchWeather(city)
    weatherData = Weather.query.filter_by(city_id = city.id).all()
    weather1 = weatherData[1]
    weather2 = weatherData[7]
    clothes = getClothes(weather1, weather2)
    return jsonify(clothes)

@app.route('/city-names', methods=['GET'])
def getCityNames():
    cities = []
    for city in City.query.all():
        cities.append(city.name)
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