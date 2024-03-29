from datetime import datetime
from flask import Flask, request, jsonify
import pytz
from clothes import create_clothes_struct, get_clothes
from base import db
from weather import *
from pollen import *
from uv import *
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from host_variables import *

app = Flask(__name__, static_folder='client', static_url_path='/')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'U0A6DRhYvG3XXgzWCUEGvu5F9UuvVCAiSYwicGbKIFpktoSb5WSgf7Fkp_YbAXhQ'


db.init_app(app)

timezone = pytz.timezone('Europe/Stockholm')
clothes_data = create_clothes_struct()


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

@app.route('/weather/<city_name>', methods=['GET'])
def one_weather(city_name):
    the_city = City.query.filter_by(name=city_name).first()
    weather = get_latest_weather(the_city)
    return jsonify(weather.serialize())


@app.route('/cities', methods=['GET'])
def getCityNames():
    cities = []
    for city in City.query.all():
        cities.append(city.serialize())
    return jsonify(cities)

@app.route('/clothes-info/<city_name>', methods=['GET'])
def get_clothes_choice(city_name):
    city = City.query.filter_by(name=city_name).first()
    if city == None:
        return jsonify('Den angivna staden finns inte.')
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

@app.route('/pollen-info/<city_name>/<value>', methods=['GET'])
def get_pollen_choice(city_name, value):
    city = City.query.filter_by(name=city_name).first()
    if city == None:
        return jsonify('Den angivna staden finns inte.')
    pollen_data = get_todays_pollen(city.latitude, city.longitude)
    return jsonify(pollen_arr[pollen_data][int(value)])

@app.route('/uv-info/<city_name>/<value>', methods=['GET'])
def get_uv_choice(city_name, value):
    city = City.query.filter_by(name=city_name).first()
    if city == None:
        return jsonify('Den angivna staden finns inte.')
    uv_data = get_todays_uv(city.latitude, city.longitude)
    print(uv_data)
    if uv_data < 2:
        return jsonify(uv_arr[0][int(value)])
    elif 2 < uv_data < 4:
        return jsonify(uv_arr[1][int(value)])
    elif 4 < uv_data < 7:
        return jsonify(uv_arr[2][int(value)])
    elif 7 < uv_data:
        return jsonify(uv_arr[3][int(value)])


def update_db_weather():
    print('uppdaterar vädret')
    with app.app_context():
        weathers = Weather.query.all()
        for weather in weathers:
            db.session.delete(weather)
            db.session.commit()
        cities_to_fetch = ['Stockholm', 'Göteborg', 'Malmö', 'Kalmar', 'Jönköping','Visby', 'Karlstad', 
        'Gävle', 'Mora', 'Sundsvall', 'Östersund', 'Umeå', 'Luleå', 'Tärnaby', 'Kiruna']
        for city_name in cities_to_fetch:
            city = City.query.filter_by(name = city_name).first()
            fetch_weather(city)
    print('uppdatering klar')

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_db_weather, trigger="interval", minutes=60)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


# update_db_weather()
if __name__ == '__main__':
    app.run(debug=True, port=3000)
