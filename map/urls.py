
from django.urls import path
from .views import *


urlpatterns = [
    path('<int:pk>/',show_map),
    #path('test_3/',),
    #path('test_4/',),
]