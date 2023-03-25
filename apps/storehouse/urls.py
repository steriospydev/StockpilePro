from django.urls import path

from . import views

app_name = 'storehouse'

urlpatterns = [
    path('',
         views.storehouse_home, name='storehouse-main'),
    path('<int:pk>/',
         views.storage_bins_page, name="storage-detail"),
    path('stock/', views.StockList.as_view(), name="stock-list"),
    path('search/',
         views.StockSearchView.as_view(), name='stock-search')
]
