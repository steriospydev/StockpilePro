from django.urls import path

from .views import CategoryListView

app_name = 'product'

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list')

]
