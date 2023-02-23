from django.urls import path

from .views import storehouse_home, storage_bins_page

app_name = 'storehouse'

urlpatterns = [
    path('', storehouse_home, name='storehouse-main'),
    path('<str:pk>/', storage_bins_page, name="storage-detail")
]
