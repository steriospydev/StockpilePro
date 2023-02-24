from django.urls import path

from .views import category_view

app_name = 'product'

urlpatterns = [
    path('categories/', category_view, name='category-list')
]
