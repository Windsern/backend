from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('buildings/<int:building_id>/', building_details),
    path('buildings/<int:building_id>/delete/', building_delete),
    path('buildings/<int:building_id>/add_to_order/', building_add_to_order),
    path('orders/<int:order_id>/', order_details),
    path('orders/<int:order_id>/delete/', order_delete),
]
