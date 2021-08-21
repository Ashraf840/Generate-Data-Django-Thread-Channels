from django.urls import path, include
from . import views


app_name = 'home'

urlpatterns = [
    path('', views.index),

    # API-url path
    path('students/api/', include('home.api.urls')),
]