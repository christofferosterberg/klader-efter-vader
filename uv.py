import requests

uv_arr = [
    ['Du behöver ingen solkräm idag :)', 'Du behöver ingen solkräm idag :)', 'Du behöver ingen solkräm idag :)'],
    ['Du behöver ingen solkräm idag', 'Du behöver ingen solkräm idag', 'Ta solskydd 10 på kroppen och 15 i ansiktet'],
    ['Du kan behöva solskydd 5 i ansiktet', 'Du kan behöva solskydd 15 i ansiktet och 10 på kroppen', 'Du kan behöva solskydd 20 i ansiktet och 15 på kroppen'],
    ['Du kan behöva solskydd 15 i ansiktet och 10 på kroppen', 'Du kan behöva solskydd 20 i ansiktet och 15 på kroppen', 'Du kan behöva solskydd 30 i ansiktet och 20 på kroppen']]

def get_todays_uv(lat, lng):
    data = requests.get('https://api.openuv.io/api/v1/uv?lat='+str(lat)+'&lng='+str(lng),
    headers={"Content-Type":"application/json", "x-access-token": '3ac3117b22b82e6e92b26b5298e47916'}).json()
    return data['result']['uv_max']