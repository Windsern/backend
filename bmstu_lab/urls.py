
from django.urls import path
from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/buildings/search/', search_building),  # GET
    path('api/buildings/<int:building_id>/', get_building_by_id),  # GET
    path('api/buildings/<int:building_id>/update/', update_building),  # PUT
    path('api/buildings/<int:building_id>/delete/', delete_building),  # DELETE
    path('api/buildings/create/', create_building),  # POST
    path('api/buildings/<int:building_id>/add_to_checking/', add_building_to_checking),  # POST
    path('api/buildings/<int:building_id>/image/', get_building_image),  # GET
    path('api/buildings/<int:building_id>/update_image/', update_building_image),  # PUT

    # Набор методов для заявок
    path('api/checkings/', get_checkings),  # GET
    path('api/checkings/<int:checking_id>/', get_checking_by_id),  # GET
    path('api/checkings/<int:checking_id>/update/', update_checking),  # PUT
    path('api/checkings/<int:checking_id>/update_status_user/', update_status_user),  # PUT
    path('api/checkings/<int:checking_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/checkings/<int:checking_id>/delete/', delete_checking),  # DELETE
    path('api/checkings/<int:checking_id>/delete_building/<int:building_id>/', delete_building_from_checking),  # DELETE

    # path("api/register/", register),
    # path("api/login/", login),
    # path("api/check/", check),
    # path("api/logout/", logout)

]
