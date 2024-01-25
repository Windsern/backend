
from django.contrib import admin
from django.urls import path, include

from bmstu_lab import views

# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# from rest_framework import permissions


# schema_view = get_schema_view(
#    openapi.Info(
#       title="Snippets API",
#       default_version='v1',
#       description="Test description",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@snippets.local"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    path('', include('bmstu_lab.urls')),
    path('admin/', admin.site.urls),

    path('build/<int:id>/', views.GetBuild, name='build_url'),
    path('', views.GetBuilds, name='building'),
    path('delete_building/', views.delete_building, name='delete_building'),

]
