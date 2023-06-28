
# map_django_project

> Данный проект реализуется ООО "Татайти" в рамках студенческого стартапа
В основе системы лежит математическая модель, обученная на двух совокупностях данных. 1-ая база данных — это перечень всех аварийных отключений за 5 лет по Республике Татарстан, 2-ая это параметры погодных условий за пять лет в разрезе метеостанций по Татарстану. Обученная модель находить закономерности между параметрами погоды и аварийными отключениями методом машинного обучения.
В рамках данного репозитория реализована DEMO-версия веб сервиса(основное решение является интеллектуальной собственностью и размещено только на сервере компании)


## Описание:

В рамках реализации веб-сервиса реалиовано веб-приложение, где был разработан веб-интерфейс интерактивной карты, также реализован сбор и обработка данных с Web API с последующем заполнением данных в DataFrame(особая структура данных библиотеки pandas).

Веб-интерфейс является интерактивной картой районов Татарстана, с возможностью выбора  значений разных периодов прогнозирования влияния погодных условий на стабильность работы электросетевых узлов, отдельных объектов карты.  

Пример работы веб-интерфейса:

![Untitled](https://github.com/kalparik/predective_monitoring/blob/main/images_for_README/map.png)

Можно заметь что визуализация прогнозирования происходит через цветовую шкалу, где зеленый-допустимое значение, оранжевый-требует внимания, красный - критическую ситуация.  Также на рисунке отображено меню выбора периода прогнозирование и описание объекта карты "Высокогорский район".


## Стек-технологий проекта.

Язык программирования:Python 

Веб-фреймворк:Django

Основные используемые библиотеки:

- Folium-библиотека для построения интерактивных карт.
- Pandas-библиотека для обработки и анализа данных.

## Структура проекта:

![Untitled](https://github.com/kalparik/predective_monitoring/blob/main/images_for_README/scheme.png)

## Обзор на проект.

### **Интерактивная карта**:

Карта разработана с помощью библиотеки Folium,координаты полигонов объектов карты хранятся в geojson формате в виде файла.

> Подробное описание кода и его реализацию можно увидеть [тут](https://github.com/kalparik/predective_monitoring/blob/main/map/views.py " ").
> 

### **Сбор данных о погодных условиях с Web API:**

> Более подробное описание кода и его реализацию можно увидеть [тут](https://github.com/kalparik/predective_monitoring/blob/master/map_api/views.py " ").
> 

Сбор данных был реализован запросом на Web API с ресурса OpenWeatherMap, далее мы десериализуем полученные json данные и вносим нужные данные в созданный DataFrame(особая структура данных библиотеки Pandas).

**Структура сбора данных:**

1. Создаем и обозначаем структуру DataFrame.

Код реализации:


    data = {'region_name': [], 'region_id': [], 'period': [], 'temp': [], 'pressure': [], 'humidity': [],
            'wind_speed': [], 'wind_gust': [], 'rain': [], 'snow': [], 'thunder': []}
    frame = pd.DataFrame(data, copy=False)


2. Запрашиваем нужные нам данные.

Код реализации:


    for i in range(45):  # цикл по индексам csv файла (45 индексов с 0 до 44)>
        API_key = "26fb96ce6ef4eb919fad5f007b318f7a"
        base_url = "https://api.openweathermap.org/data/2.5/onecall?"
        lat = str(csv_test1_data['lat'][i])
        lon = str(csv_test1_data['lon'][i])
        Final_url = base_url + "lat=" + lat + "&lon=" + lon + "&appid=" + API_key + "&exclude=minutely,alerts" + "&units=metric"

 Тут мы видим цикл где в каждой итерации запрашивается определенные данные отдельного объекта карты, объект карты обозначен как географическая координата с долготой и широтой, эти координы хранятся в ранее заготовленном csv файле.


3. После десериализации json ответа в python, подготавливаем и преобразуем нужные данные к передаче в DataFrame.

Код реализации:


    # нынешнее время
        time_current = js_obj['current']  # нынешнее данные
        time_current_dt = time_current['dt']  # Время Unix
        time_current_temp = time_current['temp']  # температура градусы
        time_current_pressure = time_current['pressure']  # атм давление в миллибарах
        time_current_humidity = time_current['humidity']  # влажность %
        time_current_wind_speed = round((time_current['wind_speed']*3.6), 3)  # Скорость ветра. Единицы измерения – км/час

 Это пример подготовки данных лишь на один период прогнозирования состояния погодных условий, также существуют другие периоды.

4. Далее заполняем данными наш DataFrame.

Код реализации:


    # Вносим нынешние данные в data frame
    now_row = {'region_name': csv_test1_data["rname"][i], 'region_id': csv_test1_data["id"][i],
               'period': 'now', 'temp': time_current_temp, 'pressure': time_current_pressure,
               'humidity': time_current_humidity,
               'wind_speed': time_current_wind_speed, 'wind_gust': time_current_wind_gust, 'rain': time_current_rain_1h,
               'snow': time_current_snow_1h, 'thunder': time_current_weather_bool_storm}

    frame = frame.append(now_row, ignore_index=True)

5. Пример частично заполненного DataFrame:

![Untitled](https://github.com/kalparik/predective_monitoring/blob/master/images_for_README/dataframe.png)

Хочется заметить что в примере отображен результат лишь одной итерации цикла, внутри которого мы собираем данные на разные промежутки прогнозирования состояния погодных условий, в последующих итерациях меняется объект карты (район татарстана), так продолжается до окончания объектов (их 45).


> Более подробное описание кода и его реализацию можно увидеть [тут](https://github.com/kalparik/predective_monitoring/blob/master/map_api/views.py " ").

##
## **Инструкции по установке:**

1. Клонируем или устанавливаем наш репозиторий в папку или PyСharm project.

 Клонируем с помощью следующей команды внутри консоли :

    git clone https://github.com/zoza99/map_django_project.git

2. Создаем и запускаем виртуальную среду с помощью следующего кода (не нужно если реализуем в PyCharm) :
   
```
    virtualenv env --no-site-packages
    
    source env/bin/activate
```
3. Переходим в нашу директорию с помощью следующего кода(если этого не сделали):

```
    cd map_django_project
```
4. Устанавливаем зависимости проекта:

```   
    pip install -r requirements.txt
```   
5. Применяем миграции:

```
    python manage.py migrate
```
6. Запускаем сервер разработки:

```
    python manage.py runserver
```
7. Далее проходим по ссылке: [http://127.0.0.1:8000/maps/0/](http://127.0.0.1:8000/maps/0/)

## Инструкция по запуску:

**Интерактивная карта**:

После установки просто пройти по этой ссылке:[http://127.0.0.1:8000/maps/0/](http://127.0.0.1:8000/maps/0/) 

**Сбор данных о погодных условиях с Web API:**

Для запуска сбора данных нужно пройти в директорию: **map_django_project\map_api**

и запустить файл **views.py**, в консоли можно будет увидеть сформированный **DataFrame**.

Это файл можно запускать независимо от проекта, для этого нужно установить библиотеку **Pandas**.
