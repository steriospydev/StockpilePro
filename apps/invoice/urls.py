from django.urls import path

from . import views

app_name = 'invoice'

urlpatterns = [
    path('', views.InvoiceList.as_view(), name='invoice-list'),
    path('<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice-detail'),
    path('create-invoice', views.invoice_create, name='invoice-create')

]
