from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('my_orders/<order_number>', views.my_orders, name='my_orders'),
]
