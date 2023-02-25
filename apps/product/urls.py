from django.urls import path

from .views import category_view, CategoryListView

app_name = 'product'

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list')

]
