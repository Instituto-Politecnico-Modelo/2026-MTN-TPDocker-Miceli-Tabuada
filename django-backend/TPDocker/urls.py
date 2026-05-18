from django.urls import path
from django.http import JsonResponse
from django.db import connection
from . import views

urlpatterns = [ #definimos las url
    path('health/', views.health),
    path('db-status/', views.db_status),
    path('items/', views.items_list, name='items_list'),
    path('items/', views.create_item, name='create_item'),
]