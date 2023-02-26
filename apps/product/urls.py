from django.urls import path

from .views import CategoryListView, CategoryDetailView, SubProductListView

app_name = 'product'

urlpatterns = [
    path('categories/', CategoryListView.as_view(),
         name='category-list'),
    path('categories/<int:pk>/subcategories', CategoryDetailView.as_view(),
         name='category-detail'),
    path('subcategories/<int:pk>/', SubProductListView.as_view(),
         name='product-sublist'),

]
