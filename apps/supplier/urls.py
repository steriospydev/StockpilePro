from django.urls import path
from .views import (SupplierListView, SupplierDetailView,
                    SupplierUpdateView, SupplierCreateView,
                    SupplierDeleteView)

app_name = 'supplier'

urlpatterns = [
    path('all/', SupplierListView.as_view(), name='supplier-list'),
    path('new/', SupplierCreateView.as_view(), name='supplier-create'),
    path('<str:pk>/', SupplierDetailView.as_view(), name='supplier-detail'),
    path('<str:pk>/edit/', SupplierUpdateView.as_view(), name='supplier-update'),
    path('<str:pk>/delete', SupplierDeleteView.as_view(), name='supplier-delete')
]
