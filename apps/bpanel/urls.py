from django.urls import path

from . import views

app_name = 'bpanel'

urlpatterns = [
    path('', views.index, name='index'),
    path('todo/delete/<int:item_id>/', views.remove, name='todo-remove'),
    path('todo/<int:item_id>/change/', views.change_status, name='todo-change'),
    path('report/', views.ops_report, name='report'),
    path('invoice-chart/', views.invoice_chart, name='invoice-chart'),
    path('product-report/', views.product_report, name='product-report')
]
