import requests
import datetime
from configparser import ConfigParser
#from config import open_weather_token
from pprint import pprint
#from api import weather
#from api import fore

parser = ConfigParser()
parser.read("settings.ini")
#parser.get('API', 'weather')

def get_wind_direction(deg):
    l = ['С ','СВ',' В','ЮВ','Ю ','ЮЗ',' З','СЗ']
    for i in range(0,8):
        step = 45.
        min = i*step - 45/2.
        max = i*step + 45/2.
        if i == 0 and deg > 360-45/2.:
            deg = deg - 360
        if deg >= min and deg <= max:
            res = l[i]
            break
    return res

def get_weather(city, open_weather_token):
    try:
        #if day == false:
            #r = requests.get(
            #   f"{url_base}?q={city}&appid={open_weather_token}&units=metric"
            r = requests.get( parser.get('API', 'weather'),
                params = {'q': city, 'appid': parser.get('token', 'open_weather_token'), 'units': 'metric'}
            )
            data = r.json()
            #pprint(data)

            city = data["name"]
            cur_weather = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            zoo_day =datetime.datetime.fromtimestamp(data["sys"]["sunset"])-datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            idid = data["id"]
            #long = data["coord"]["lon"]
            #lati = data["coord"]["lat"]

            print(f"Прогноз погоды на {datetime.datetime.now().strftime('%A, %d %B')}\n"
                f"Город: {city}\nТемпература: {cur_weather} ℃\n"
                f"Влажность:{humidity} %\nДавление: {pressure} мм. рт. ст\nВетер: {wind} м/c\n"
                f"Рассвет: {sunrise.strftime('%H:%M')}\nЗакат: {sunset.strftime('%H:%M')}\n"
                f"Продолжительность дня: {zoo_day}"
                )

            otvet = input("Посмотрим прогноз погоды? True or False?")

            if otvet == "True":

                r = requests.get( parser.get('API', 'fore'),
                                 params={'id': idid , 'appid': parser.get('token', 'open_weather_token'), 'units': 'metric'}
                                 )
                data = r.json()

                city = data["city"]["name"]
                for i in data['list']:
                    print((i['dt_txt'])[:16], '{0:+3.0f}'.format(i['main']['temp'])+ "℃",
                          '{0:2.0f}'.format(i['wind']['speed']) + "м/с",
                          get_wind_direction(i['wind']['deg']),
                          i['weather'][0]['description'])
            else:
                print("Всего доброго!")

    except Exception as ex:
        print("Проверьте название города!")

def main():
    city = input("Введите город для просмотра текущей погоды: ")
    get_weather(city, parser.get('token', 'open_weather_token'))
#    #forecast(id, open_weather_token)


if __name__ == '__main__':
    main()