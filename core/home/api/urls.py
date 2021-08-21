from django.urls import path
from . import views


urlpatterns = [
    path('test/', views.generate_student_data_test),
    path('create_dummy_student_data/', views.generate_student_data), # pass a param ("total") specifying an integer
]