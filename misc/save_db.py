import json
from app import City

# This program saves the current db to json-file. Only used once.

cities = []
for city in City.query.all():
    cities.append(city.serialize())

json_string = json.dumps(cities, indent=4, sort_keys=True)

save_file = open('all_cities.json', 'w')
save_file.write(json_string)
save_file.close()
