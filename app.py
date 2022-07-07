from datetime import datetime
from flask import Flask, request, jsonify
import pytz
from clothes import create_clothes_struct, get_clothes
from base import db
from weather import *
from pollen import *

app = Flask(__name__, static_folder='client', static_url_path='/')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'U0A6DRhYvG3XXgzWCUEGvu5F9UuvVCAiSYwicGbKIFpktoSb5WSgf7Fkp_YbAXhQ'

db.init_app(app)

timezone = pytz.timezone('Europe/Stockholm')
clothes_data = create_clothes_struct()

host = 'http://localhost:3000'


######## ROUTES ##############

@app.route('/')
def client():
    return app.send_static_file('client.html')


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        wanted_cities = request.json
        weather_data = []
        for city in wanted_cities:
            the_city = City.query.filter_by(name=city).first()
            weather = get_latest_weather(the_city)
            weather_data.append(weather.serialize())
        return jsonify(weather_data)


@app.route('/cities', methods=['GET'])
def getCityNames():
    cities = []
    for city in City.query.all():
        cities.append(city.serialize())
    return jsonify(cities)

@app.route('/clothes-info/<city_name>', methods=['GET'])
def get_clothes_choice(city_name):
    city = City.query.filter_by(name=city_name).first()
    weather = get_todays_weather(city)
    weather1 = get_clothes(weather[1])
    if datetime.now().hour <= 17:
        weather2 = get_clothes(weather[7])
        if weather1 == weather2:
            return jsonify('Ta på dig '+ weather1)
        else:
            return jsonify('Ta på dig ' + weather1 + ' Ta även med dig ' + weather2)
    else:
        return jsonify('Ta på dig '+ weather1)

pollen_arr = [
    ['Du behöver inte ta någon pollenmedicin idag :)', 'Du behöver inte ta någon pollenmedicin idag :)', 'Om du är extremt allergisk och kan ha andningssvårigheter kan det vara bra med lite medicin idag'],
    ['Du behöver inte ta någon pollenmedicin idag :)', 'Om du inte har några andningsbesvär generellt behöver du inte ta någon medicin idag', 'Idag kan det vara klokt att ta medicin'],
    ['Idag kan det vara klokt att ta medicin', 'Idag kan det vara klokt att ta medicin', 'Idag kan det vara klokt att ta medicin'],
    ['Pollenregn idag! Ta din medicin', 'Pollenregn idag! Ta din medicin', 'Pollenregn idag! Ta din medicin']]
@app.route('/pollen-info/<city_name>/<value>', methods=['GET'])
def get_pollen_choice(city_name, value):
    city = City.query.filter_by(name=city_name).first()
    pollen_data = get_todays_pollen(city.latitude, city.longitude)
    return jsonify(pollen_arr[pollen_data][int(value)])

@app.route('/uv-info/<city_name>/<value>', methods=['GET'])
def get_uv_choice(city_name, value):
    city = City.query.filter_by(name=city_name).first()
    return jsonify('hejdå')
#     weather = get_todays_weather(city)
#     weather1 = get_clothes(weather[1])
#     if datetime.now().hour <= 17:
#         weather2 = get_clothes(weather[7])
#         if weather1 == weather2:
#             return jsonify('Ta på dig '+ weather1)
#         else:
#             return jsonify('Ta på dig ' + weather1 + ' Ta även med dig ' + weather2)
#     else:
#         return jsonify('Ta på dig '+ weather1)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
