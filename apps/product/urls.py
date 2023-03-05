from django.urls import path

from . import views

app_name = 'product'

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(),
         name='category-list'),
    path('categories/<int:pk>/subcategories', views.CategoryDetailView.as_view(),
         name='category-detail'),
    path('subcategories/<int:pk>/', views.SubProductListView.as_view(),
         name='product-sublist'),
    path('subcategories/new_product/', views.ProductCreateView.as_view(),
         name='product-create'),
    path('categories/new/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
    path('categories/<int:category_id>/subcatecory/create',
         views.SubCategoryCreateView.as_view(),
         name='subcategory-create'),
    path('categories/<int:category_id>/subcatecory/<int:pk>',
         views.SubCategoryUpdateView.as_view(),
         name='subcategory-update'),
    # product-list
    # product-update
    # product-delete
    # product-detail
    path('all/', views.ProductList.as_view(), name='product-list'),
    path('new/', views.ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete', views.ProductDeleteView.as_view(), name='product-delete'),
    path('search/', views.ProductSearchView.as_view(), name='product-search')
]
