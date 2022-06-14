from datetime import datetime
from flask import Flask
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__, static_folder='client', static_url_path='/')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'U0A6DRhYvG3XXgzWCUEGvu5F9UuvVCAiSYwicGbKIFpktoSb5WSgf7Fkp_YbAXhQ'
db = SQLAlchemy(app)

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

    city_id     = db.Column(db.Integer, ForeignKey('city.id'))

    def __repr__(self):
        return '<Weather {}: {} {} {} {} {}>'.format(self.id, self.datetime, self.description, self.temperature, self.windSpeed, self.city_id)

    def serialize(self):
        return dict(id=self.id, datetime=self.datetime, description=self.description, temperature=self.temperature, windSpeed=self.windSpeed, city_id=self.city_id)
    



# db.init_app(app)

host = "http://localhost:3000"

def getWeatherData():
    return requests.get('https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/12/lat/58/data.json').json()

@app.route("/")
def client():
    print(getWeatherData())
    return app.send_static_file("client.html")

if __name__ == '__main__':
    app.run(debug=True, port=3000)