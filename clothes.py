
chilly = 0
warm = 10
hot = 20
rain = 0.1
heavy_rain = 1.0
cloudy = 5
windy = 5.0

class Last_Node:
    def __init__(self, texts):
        self.texts = texts
    def find_clothes(self, data):
        return self.texts[0]

class Node:
    def __init__(self, search_word, answer):
        self.yes = None
        self.no = None
        self.search_word = search_word
        self.answer = answer

    def insert(self, search_word, answer, level, answers):
        if answers[level] == 'yes':
            if self.yes is None:
                self.yes = Node(search_word, answer)
            else:
                self.yes.insert(search_word, answer, level-1, answers)
        else:
            if self.no is None:
                self.no = Node(search_word, answer)
            else:
                self.no.insert(search_word, answer, level-1, answers)
    

    def insert_last(self, level, answers, texts):
        if level == 0:
            if answers[0] == 'yes':
                self.yes = Last_Node(texts)
            else:
                self.no = Last_Node(texts)
        else:
            if answers[level] == 'yes':
                self.yes.insert_last(level-1, answers, texts)
            else:
                self.no.insert_last(level-1, answers, texts)

    def find_clothes(self, weather_data):
        if weather_data[self.search_word] > self.answer:
            return self.yes.find_clothes(weather_data)
        else:
            return self.no.find_clothes(weather_data)

def create_clothes_struct():
    root = Node('temperature', warm)
    root.insert('temperature', hot, 0, ['yes'])
    root.insert('temperature', chilly, 0, ['no'])
    root.insert('precipitation', rain, 1, ['yes', 'yes'])
    root.insert('precipitation', heavy_rain, 2, ['yes', 'yes', 'yes'])
    root.insert('cloudiness', cloudy, 1, ['no', 'yes'])
    root.insert('wind_speed', windy, 2, ['no', 'no', 'yes'])
    root.insert('precipitation', rain, 2, ['yes', 'no', 'yes'])
    root.insert('precipitation', heavy_rain, 3, ['yes', 'yes', 'no', 'yes'])
    root.insert('wind_speed', windy, 3, ['no', 'yes', 'no', 'yes'])


    root.insert_last(3, ['yes', 'yes', 'yes', 'yes'], ['en tunn regnjacka eller paraply.'])
    root.insert_last(3, ['no', 'yes', 'yes', 'yes'], ['l??ngbyxor och l??ngtr??ja, ta med n??got mot regn ifall att.'])
    root.insert_last(2, ['no', 'yes', 'yes'], ['shorts eller kjol och en go t-shirt.'])
    root.insert_last(4, ['yes', 'yes', 'yes', 'no', 'yes'], ['paraply och regnjacka, ta inga ljusa byxor d??r det syns om de blir bl??ta.'])
    root.insert_last(4, ['no', 'yes', 'yes', 'no', 'yes'], ['en regnjacka och l??ngbyxor.'])
    root.insert_last(4, ['yes', 'no', 'yes', 'no', 'yes'], ['en tunn jacka mot vinden eller varma kl??der, det ska bl??sa.'])
    root.insert_last(4, ['no', 'no', 'yes', 'no', 'yes'], ['en tunn l??ng??rmad tr??ja och ett par l??ngbyxor.'])
    root.insert_last(3, ['yes', 'no', 'no', 'yes'], ['en tunn l??ng??rmad tr??ja och ett par l??ngbyxor, det ska bl??sa en del trots solen.'])
    root.insert_last(3, ['no', 'no', 'no', 'yes'], ['shorts och en go t-shirt.'])

    return root

def get_clothes(weather):
    from app import clothes_data
    
    weather_data = {
        'temperature'    : weather.temperature,
        'cloudiness'     : weather.cloudiness,
        'precipitation'  : weather.precipitation,
        'wind_speed'     : weather.wind_speed
    }
    return clothes_data.find_clothes(weather_data)