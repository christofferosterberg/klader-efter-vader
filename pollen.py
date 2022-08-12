import requests

pollen_arr = [
    ['Du behöver inte ta någon pollenmedicin idag :)', 'Du behöver inte ta någon pollenmedicin idag :)', 'Om du är extremt allergisk och kan ha andningssvårigheter kan det vara bra med lite medicin idag'],
    ['Du behöver inte ta någon pollenmedicin idag :)', 'Om du inte har några andningsbesvär generellt behöver du inte ta någon medicin idag', 'Idag kan det vara klokt att ta medicin'],
    ['Idag kan det vara klokt att ta medicin', 'Idag kan det vara klokt att ta medicin', 'Idag kan det vara klokt att ta medicin'],
    ['Pollenregn idag! Ta din medicin', 'Pollenregn idag! Ta din medicin', 'Pollenregn idag! Ta din medicin']]

translate = {
    "Low": 0,
    "Moderate": 1,
    "High": 2,
    "Very High": 3
}
def get_todays_pollen(latitude, longitude):
    data = requests.get('https://api.ambeedata.com/latest/pollen/by-lat-lng?lat='+str(latitude)+'&lng='+str(longitude),
    headers={"Content-Type":"application/json", "x-api-key": 'e68ed44d9f2f0b3532af15d811549032a807063658f82cca642a229ce9a95832'}).json()
    grass=translate[data['data'][0]['Risk']['grass_pollen']]
    tree=translate[data['data'][0]['Risk']['tree_pollen']]
    weed=translate[data['data'][0]['Risk']['weed_pollen']]
    values = [grass, tree, weed]
    return max(values)