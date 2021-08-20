from django.urls import path
from . import views


urlpatterns = [
    path('test/', views.generate_student_data_test),
]