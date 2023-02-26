from django.urls import path

from .views import CategoryListView, CategoryDetailView

app_name = 'product'

urlpatterns = [
    path('categories/', CategoryListView.as_view(),
         name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(),
         name='category-detail'),

]
