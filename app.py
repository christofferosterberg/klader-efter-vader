from datetime import datetime
from flask import Flask
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import pytz

app = Flask(__name__, static_folder='client', static_url_path='/')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'U0A6DRhYvG3XXgzWCUEGvu5F9UuvVCAiSYwicGbKIFpktoSb5WSgf7Fkp_YbAXhQ'
db = SQLAlchemy(app)

timezone = pytz.timezone("Europe/Stockholm")

host = "http://localhost:3000"


# Classes in db
class City(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(80), unique=True, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude  = db.Column(db.Float, nullable=False)
    weathers  = relationship('Weather')

    def __repr__(self):
        return '<City {}: {} {} {}>'.format(self.id, self.name, self.longitude, self.latitude)

    def serialize(self):
        return dict(id=self.id, name=self.name, longitude=self.longitude, latitude=self.latitude)

class Weather(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    datetime    = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text(20), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    windSpeed   = db.Column(db.Float, nullable=False)

    city_id   = db.Column(db.Integer, ForeignKey('city.id'))

    def __repr__(self):
        return '<Weather {}: {} {} {} {} {}>'.format(self.id, self.datetime, self.description, self.temperature, self.windSpeed, self.city_id)

    def serialize(self):
        return dict(id=self.id, datetime=self.datetime, description=self.description, temperature=self.temperature, windSpeed=self.windSpeed, city_id=self.city_id)
    




#Gets a datetime in string format "YYYY-MM-DD HH:MM:SS"
def str_datetime(datetime_string):
    if datetime_string is None:
        return datetime_string
    if isinstance(datetime_string, datetime):
        return datetime_string
    date_time = timezone.localize(datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S'))
    return date_time


def getWeatherData():

    cities = City.query.all()
    print(cities)

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
            description = parameters[18]['values'][0]
            temperature = parameters[1]['values'][0]
            windSpeed   = parameters[4]['values'][0]

            newWeather = Weather(datetime=str_datetime(dt), description=description, temperature=temperature, windSpeed=windSpeed, city_id=city.id)
            db.session.add(newWeather)
    
    db.session.commit()



@app.route("/")
def client():
    getWeatherData()
    return app.send_static_file("client.html")

if __name__ == '__main__':
    app.run(debug=True, port=3000)