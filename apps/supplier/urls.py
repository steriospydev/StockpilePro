from django.urls import path
from .views import (SupplierListView, SupplierDetailView,
                    SupplierUpdateView, SupplierCreateView,
                    SupplierDeleteView, SupplierSearchView)

app_name = 'supplier'

urlpatterns = [
    path('', SupplierListView.as_view(), name='supplier-list'),
    path('new/', SupplierCreateView.as_view(), name='supplier-create'),
    path('<int:pk>/', SupplierDetailView.as_view(), name='supplier-detail'),
    path('<int:pk>/edit/', SupplierUpdateView.as_view(), name='supplier-update'),
    path('<int:pk>/delete', SupplierDeleteView.as_view(), name='supplier-delete'),
    path('search/', SupplierSearchView.as_view(), name='supplier-search')

]
