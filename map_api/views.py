import datetime, time
import json
import urllib.request, urllib.parse
import pandas as pd
from statistics import mean

# настройки отображения датафрейма в консоли
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

csv_test1_data = pd.read_csv("test_map_coord_2.csv")  # считываем csv файл через pandas

# создание датафрейма
data = {'region_name': [], 'region_id': [], 'period': [], 'temp': [], 'pressure': [], 'humidity': [],
        'wind_speed': [], 'wind_gust': [], 'rain': [], 'snow': [], 'thunder': []}
frame = pd.DataFrame(data, copy=False)

for i in range(45):  # цикл по индексам csv файла (45 индексов с 0 до 44)
    API_key = "26fb96ce6ef4eb919fad5f007b318f7a"
    base_url = "https://api.openweathermap.org/data/2.5/onecall?"
    lat = str(csv_test1_data['lat'][i])
    lon = str(csv_test1_data['lon'][i])

    Final_url = base_url + "lat=" + lat + "&lon=" + lon + "&appid=" + API_key + "&exclude=minutely,alerts" + "&units=metric"

    data = urllib.request.urlopen(Final_url).read()  # Считываем json
    js_obj = json.loads(data)  # десериализует str json в объекты python

    # начинаем парсить данный с js_obj

    # нынешнее время
    time_current = js_obj['current']  # нынешнее данные
    time_current_dt = time_current['dt']  # Время Unix
    time_current_temp = time_current['temp']  # температура градусы
    time_current_pressure = time_current['pressure']  # атм давление в миллибарах
    time_current_humidity = time_current['humidity']  # влажность %
    time_current_wind_speed = round((time_current['wind_speed']*3.6), 3)  # Скорость ветра. Единицы измерения – км/час
    if 'wind_gust' in time_current.keys():
        time_current_wind_gust = round(time_current['wind_gust']*3.6, 3)  # Порыв ветра. Единицы измерения – км/час
    else:
        time_current_wind_gust = 0
    if 'rain' in time_current.keys():
        time_current_rain = time_current['rain']
        time_current_rain_1h = time_current_rain['1h']  # (при наличии) Объем осадков, мм
    else:
        time_current_rain_1h = 0  # можно 0

    if 'snow' in time_current.keys():
        time_current_snow = time_current['snow']
        time_current_snow_1h = time_current_snow['1h']  # (при наличии) Объем снега, мм
    else:
        time_current_snow_1h = 0  # можно 0

    time_current_weather = time_current['weather']
    time_current_weather_list = time_current_weather[0]
    time_current_weather_id = time_current_weather_list['id']

    if time_current_weather_id in [200, 201, 202, 210, 211, 212, 221, 230, 231, 232]:  # если id 2хх то гроза была
        time_current_weather_bool_storm = 1

    else:
        time_current_weather_bool_storm = 0

        # пример с переводом Unix в datetime и отбрасыванием не нужных значений времени
        value = datetime.datetime.fromtimestamp(time_current_dt)  # преобразует Unix в datetime
        value_rep = value.replace(minute=0, second=0)  # Отбрасываем значение минут и секунд на 0
        value_rep_str = value_rep.strftime(
            '%Y-%m-%d %H:%M:%S')  # конвертируем datetime в форму str для использования в след преобразовании
        value_rep_unix = int(time.mktime(datetime.datetime.strptime(value_rep_str,
             "%Y-%m-%d %H:%M:%S").timetuple()))  # используем str форму для перевода в Unix

    # через 3 ч
    time_h = js_obj['hourly']  # погодные условия на промежутки в час
    time_hourly3 = time_h[3]  # погодные условия через 3 ч
    time_hourly3_dt = time_hourly3['dt']  # время в Unix
    time_hourly3_temp = time_hourly3['temp']  # температура градусы
    time_hourly3_pressure = time_hourly3['pressure']  # атм давление в миллибарах
    time_hourly3_humidity = time_hourly3['humidity']  # влажность %
    time_hourly3_wind_speed = round(time_hourly3['wind_speed']*3.6, 3) # Скорость ветра. Единицы измерения – км/час

    if 'wind_gust' in time_hourly3.keys():
        time_hourly3_wind_gust = round(time_hourly3['wind_gust']*3.6, 3)  # Порыв ветра. Единицы измерения – км/час
    else:
        time_hourly3_wind_gust = 0

    if 'rain' in time_hourly3.keys():
        time_hourly3_rain = time_hourly3['rain']  # (при наличии) Объем осадков, мм
        time_hourly3_rain_1h = time_hourly3_rain['1h']
    else:
        time_hourly3_rain_1h = 0

    if 'snow' in time_hourly3.keys():
        time_hourly3_snow = time_hourly3['snow']  # (при наличии) Объем снега, мм
        time_hourly3_snow_1h = time_hourly3_snow['1h']
    else:
        time_hourly3_snow_1h = 0

    time_hourly3_weather = time_hourly3['weather']
    time_hourly3_weather_list = time_hourly3_weather[0]
    time_hourly3_weather_id = time_hourly3_weather_list['id']

    if time_hourly3_weather_id in [200, 201, 202, 210, 211, 212, 221, 230, 231, 232]:  # если id 2хх то гроза была
        time_hourly3_weather_bool_storm = 1
    else:
        time_hourly3_weather_bool_storm = 0

    # через 12 ч
    time_hourly12 = time_h[12]  # погодные условия через 12 ч
    time_hourly12_dt = time_hourly12['dt']  # время в Unix
    time_hourly12_temp = time_hourly12['temp']  # температура градусы
    time_hourly12_pressure = time_hourly12['pressure']  # атм давление в миллибарах
    time_hourly12_humidity = time_hourly12['humidity']  # влажность %
    time_hourly12_wind_speed = round(time_hourly12['wind_speed']*3.6, 3)  # Скорость ветра. Единицы измерения – км/час

    if 'wind_gust' in time_hourly12.keys():
        time_hourly12_wind_gust = round(time_hourly12['wind_gust']*3.6, 3)  # Порыв ветра. Единицы измерения – км/час
    else:
        time_hourly12_wind_gust = 0

    if 'rain' in time_hourly12.keys():
        time_hourly12_rain = time_hourly12['rain']  # (при наличии) Объем осадков, мм
        time_hourly12_rain_1h = time_hourly12_rain['1h']
    else:
        time_hourly12_rain_1h = 0

    if 'snow' in time_hourly12.keys():
        time_hourly12_snow = time_hourly12['snow']  # (при наличии) Объем снега, мм
        time_hourly12_snow_1h = time_hourly12_snow['1h']
    else:
        time_hourly12_snow_1h = 0

    time_hourly12_weather = time_hourly12['weather']
    time_hourly12_weather_list = time_hourly12_weather[0]
    time_hourly12_weather_id = time_hourly12_weather_list['id']

    if time_hourly12_weather_id in [200, 201, 202, 210, 211, 212, 221, 230, 231, 232]:  # если id 2хх то гроза была
        time_hourly12_weather_bool_storm = 1
    else:
        time_hourly12_weather_bool_storm = 0

    # через 1 день
    time_daily = js_obj['daily']  # погодные условия с промежутком в дни
    time_daily1 = time_daily[1]
    time_daily1_dt = time_daily1['dt']  # Время Unix
    time_daily1_temp = time_daily1['temp']  # значения температур а градусах
    time_daily1_temp_min = time_daily1_temp['min']  # min температура градусы
    time_daily1_temp_max = time_daily1_temp['max']  # max температура градусы
    time_daily1_temp_avg = round((mean([time_daily1_temp_min, time_daily1_temp_max])), 2)  # среднее арифметическое max и min температуры
    time_daily1_pressure = time_daily1['pressure']  # атм давление в миллибарах
    time_daily1_humidity = time_daily1['humidity']  # влажность %
    time_daily1_wind_speed = round(time_daily1['wind_speed']*3.6, 3)  # Скорость ветра. Единицы измерения – км/час

    if 'wind_gust' in time_daily1.keys():
        time_daily1_wind_gust = round(time_daily1['wind_gust']*3.6, 3)  # Порыв ветра. Единицы измерения – км/час
    else:
        time_daily1_wind_gust = 0

    if 'rain' in time_daily1.keys():
        time_daily1_rain = time_daily1['rain']  # (при наличии) Объем осадков, мм
        #time_daily1_rain_1h = time_daily1_rain['1h']
    else:
        time_daily1_rain = 0

    if 'snow' in time_daily1.keys():
        time_daily1_snow = time_daily1['snow']  # (при наличии) Объем снега, мм
        #time_daily1_snow_1h = time_daily1_snow['1h']
    else:
        time_daily1_snow = 0

    time_daily1_weather = time_daily1['weather']
    time_daily1_weather_list = time_daily1_weather[0]
    time_daily1_weather_id = time_daily1_weather_list['id']

    if time_daily1_weather_id in [200, 201, 202, 210, 211, 212, 221, 230, 231, 232]:  # если id 2хх то гроза была
        time_daily1_weather_bool_storm = 1
    else:
        time_daily1_weather_bool_storm = 0

    # через 3 дня
    time_daily3 = time_daily[3]
    time_daily3_dt = time_daily3['dt']  # Время Unix
    time_daily3_temp = time_daily3['temp']  # значения температур в градусах
    time_daily3_temp_min = time_daily3_temp['min']  # min температура градусы
    time_daily3_temp_max = time_daily3_temp['max']  # max температура градусы
    time_daily3_temp_avg = round((mean([time_daily3_temp_min, time_daily3_temp_max])), 2)  # среднее арифметическое max и min температуры
    time_daily3_pressure = time_daily3['pressure']  # атм давление в миллибарах
    time_daily3_humidity = time_daily3['humidity']  # влажность %
    time_daily3_wind_speed = round(time_daily3['wind_speed']*3.6, 3)  # Скорость ветра. Единицы измерения – км/час

    if 'wind_gust' in time_daily3.keys():
        time_daily3_wind_gust = round(time_daily3['wind_gust']*3.6, 3)  # Порыв ветра. Единицы измерения – км/час
    else:
        time_daily3_wind_gust = 1

    if 'rain' in time_daily3.keys():
        time_daily3_rain = time_daily3['rain']  # (при наличии) Объем осадков, мм
    else:
        time_daily3_rain = 0

    if 'snow' in time_daily3.keys():
        time_daily3_snow = time_daily3['snow']  # (при наличии) Объем снега, мм
    else:
        time_daily3_snow = 0

    time_daily3_weather = time_daily3['weather']
    time_daily3_weather_list = time_daily3_weather[0]
    time_daily3_weather_id = time_daily3_weather_list['id']

    if time_daily3_weather_id in [200, 201, 202, 210, 211, 212, 221, 230, 231, 232]:  # если id 2хх то гроза была
        time_daily3_weather_bool_storm = 1
    else:
        time_daily3_weather_bool_storm = 0

    # Вносим нынешние данные в data frame
    now_row = {'region_name': csv_test1_data["rname"][i], 'region_id': csv_test1_data["id"][i],
               'period': 'now', 'temp': time_current_temp, 'pressure': time_current_pressure,
               'humidity': time_current_humidity,
               'wind_speed': time_current_wind_speed, 'wind_gust': time_current_wind_gust, 'rain': time_current_rain_1h,
               'snow': time_current_snow_1h, 'thunder': time_current_weather_bool_storm}

    frame = frame.append(now_row, ignore_index=True)

    # Вносим прогнозируемые данные в data frame(3 часа)
    h3_row = {'region_name': csv_test1_data["rname"][i], 'region_id': csv_test1_data["id"][i],
               'period': '3h', 'temp': time_hourly3_temp, 'pressure': time_hourly3_pressure,
               'humidity': time_hourly3_humidity,
               'wind_speed': time_hourly3_wind_speed, 'wind_gust': time_hourly3_wind_gust, 'rain': time_hourly3_rain_1h,
               'snow': time_hourly3_snow_1h, 'thunder': time_hourly3_weather_bool_storm}

    frame = frame.append(h3_row, ignore_index=True)

    # Вносим прогнозируемые данные в data frame(12 часов)
    h12_row = {'region_name': csv_test1_data["rname"][i], 'region_id': csv_test1_data["id"][i],
              'period': '12h', 'temp': time_hourly12_temp, 'pressure': time_hourly12_pressure,
              'humidity': time_hourly12_humidity,
              'wind_speed': time_hourly12_wind_speed, 'wind_gust': time_hourly12_wind_gust, 'rain': time_hourly12_rain_1h,
              'snow': time_hourly12_snow_1h, 'thunder': time_hourly12_weather_bool_storm}

    frame = frame.append(h12_row, ignore_index=True)

    # Вносим прогнозируемые данные в data frame(1 день)
    d1_row = {'region_name': csv_test1_data["rname"][i], 'region_id': csv_test1_data["id"][i],
               'period': '1d', 'temp': time_daily1_temp_avg, 'pressure': time_daily1_pressure,
               'humidity': time_daily1_humidity,
               'wind_speed': time_daily1_wind_speed, 'wind_gust': time_daily1_wind_gust, 'rain': time_daily1_rain,
               'snow': time_daily1_snow, 'thunder': time_daily1_weather_bool_storm}

    frame = frame.append(d1_row, ignore_index=True)

    # Вносим прогнозируемые данные в data frame(3 дня)
    d3_row = {'region_name': csv_test1_data["rname"][i], 'region_id': csv_test1_data["id"][i],
              'period': '3d', 'temp': time_daily3_temp_avg, 'pressure': time_daily3_pressure,
              'humidity': time_daily3_humidity,
              'wind_speed': time_daily3_wind_speed, 'wind_gust': time_daily3_wind_gust, 'rain': time_daily3_rain,
              'snow': time_daily3_snow, 'thunder': time_daily3_weather_bool_storm}

    frame = frame.append(d3_row, ignore_index=True)


new_frame = frame.copy(deep=True)  # Создаем копию dataframe
print(frame)
