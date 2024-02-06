from django.urls import path
from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/buildings/search/', search_buildings),  # GET
    path('api/buildings/<int:building_id>/', get_building_by_id),  # GET
    path('api/buildings/<int:building_id>/image/', get_building_image),  # GET
    path('api/buildings/<int:building_id>/update/', update_building),  # PUT
    path('api/buildings/<int:building_id>/update_image/', update_building_image),  # PUT
    path('api/buildings/<int:building_id>/delete/', delete_building),  # DELETE
    path('api/buildings/create/', create_building),  # POST
    path('api/buildings/<int:building_id>/add_to_verification/', add_building_to_verification),  # POST

    # Набор методов для заявок
    path('api/verifications/search/', search_verifications),  # GET
    path('api/verifications/<int:verification_id>/', get_verification_by_id),  # GET
    path('api/verifications/<int:verification_id>/update/', update_verification),  # PUT
    path('api/verifications/<int:verification_id>/update_status_user/', update_status_user),  # PUT
    path('api/verifications/<int:verification_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/verifications/<int:verification_id>/delete/', delete_verification),  # DELETE
    path('api/verifications/<int:verification_id>/delete_building/<int:building_id>/', delete_building_from_verification), # DELETE
    path('api/verifications/<int:verification_id>/update_building/<int:building_id>/', update_building_in_verification), # PUT

    # Набор методов для аутентификации и авторизации
    path("api/register/", register),
    path("api/login/", login),
    path("api/verification/", verification),
    path("api/logout/", logout)
]
