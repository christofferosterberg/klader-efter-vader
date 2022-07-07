import requests
from api_keys import AMBEE_KEY
translate = {
    "Low": 0,
    "Moderate": 1,
    "High": 2,
    "Very High": 3
}
def get_todays_pollen(latitude, longitude):
    data = requests.get('https://api.ambeedata.com/latest/pollen/by-lat-lng?lat='+str(latitude)+'&lng='+str(longitude),
    headers={"Content-Type":"application/json", "x-api-key": AMBEE_KEY}).json()
    grass=translate[data['data'][0]['Risk']['grass_pollen']]
    tree=translate[data['data'][0]['Risk']['tree_pollen']]
    weed=translate[data['data'][0]['Risk']['weed_pollen']]
    values = [grass, tree, weed]
    return max(values)