import folium
from django.shortcuts import render
import pandas as pd
import json

with open("all_id_new.geojson", "r",  encoding='utf-8') as read_file:  # фиксит проблему с инкодингом русских слов
     encod_geo_data = json.load(read_file)  # (десериализует json в объекты python)

def show_map(request, pk):

    m = folium.Map(location=[55.17, 51.00], tiles="OpenStreetMap", name="Light Map", height='100%',
                   zoom_start=7.5, zoom_control=False,
               scrollWheelZoom=False, dragging=False,inertia=False)  # настройки отображения веб-карты

    csv_test_data = pd.read_csv("csv_test_map_3.csv")
    # через pandas подгружаем возможность прочесть тестовые значения

    choice = ['Test_1', 'Test_2', 'Test_3', 'Test_4', 'Test_5']  # значения выбора
    choice_period = ['Now(Test_1)', '3h(Test_2)', '12h(Test_3)', '1d(Test_4)', '3d(Test_5)']
    period = choice_period[pk]

    folium.Choropleth(
        geo_data="all_id_new.geojson",   # можно поменять на encod_geo_data, если нужно будет работать с русским текстом
        name="choropleth",
        data=csv_test_data,  # подключение файла с тестовыми данными
        columns=["id",choice[pk]],  # прописываем внешний ключ
        key_on="feature.properties.id",  # прописываем первичный ключ
       fill_color="YlOrRd",  # Вбираем цветовую градацию отображения изменений
        fill_opacity=0.7,
        line_opacity=.1,
    ).add_to(m)

    folium.features.GeoJson(data=encod_geo_data,  # Выбираем файл для работы с данными
     name="States", popup=folium.features.GeoJsonPopup(fields=["rname", "id"],  # Выбираем данные для отображения
      aliases=["region_name", "region_id"])).add_to(m)  # Выбираем данные для отображения
    m = m._repr_html_()
    context = {'my_map': m,
               'period': period
               }


    return render(request, 'map/map_render.html', context)



