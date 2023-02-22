from django.urls import path

from .views import storehouse_home

app_name = 'storehouse'

urlpatterns = [
    path('', storehouse_home, name='storehouse-main')
]
