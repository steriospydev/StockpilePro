from django.urls import path

from .views import (CategoryListView, CategoryDetailView, SubProductListView,
                    CategoryCreateView, CategoryUpdateView, CategoryDeleteView)

app_name = 'product'

urlpatterns = [
    path('categories/', CategoryListView.as_view(),
         name='category-list'),
    path('categories/<int:pk>/subcategories', CategoryDetailView.as_view(),
         name='category-detail'),
    path('subcategories/<int:pk>/', SubProductListView.as_view(),
         name='product-sublist'),
    path('categories/new/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

]
