from django.urls import path

from . import views

app_name = 'bpanel'

urlpatterns = [
    path('', views.index, name='index'),
    path('todo/delete/<int:item_id>/', views.remove, name='todo-remove'),
    path('todo/<int:item_id>/change/', views.change_status, name='todo-change'),
    path('report/', views.ops_report, name='report')
]
