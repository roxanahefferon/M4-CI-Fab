from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_catalogue, name='catalogue'),
    path('<int:product_id>/', views.product_description,
         name='product_description'),
    path('create_product/', views.create_product, name='create_product'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
]
