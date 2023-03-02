from django.urls import path
from .views import *

urlpatterns = [
    path('/get_teachers', getTeachers, name="getTeachers"),
    path('/add_teacher', addTeacher, name="addTeacher"),
    path('/get_teacher', getTeacher, name="getTeacher"),
]