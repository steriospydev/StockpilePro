from django.urls import path

from .views import (CategoryListView, CategoryDetailView, SubProductListView,
                    CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
                    ProductCreateView)

app_name = 'product'

urlpatterns = [
    path('categories/', CategoryListView.as_view(),
         name='category-list'),
    path('categories/<int:pk>/subcategories', CategoryDetailView.as_view(),
         name='category-detail'),
    path('subcategories/<int:pk>/', SubProductListView.as_view(),
         name='product-sublist'),
    path('subcategories/new_product/', ProductCreateView.as_view(),
         name='product-create'),
    path('categories/new/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),


]
