from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_catalogue, name='catalogue'),
    path('<int:product_id>/', views.product_description,
         name='product_description'),
    path('create/', views.product_create, name='product_create'),
]
