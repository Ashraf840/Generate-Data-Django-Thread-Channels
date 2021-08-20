from django.urls import path, include
from . import views


app_name = 'home'

urlpatterns = [
    path('', views.index),

    # API-url path
    path('students/', views.generate_student_data), # pass a param ("total") specifying an integer

    path('students/api/', include('home.api.urls')),
]