from django.urls import path
from .views import *

urlpatterns = [
    path("/get_csrf", generate_csrf_token, name="generate_csrf_token"),
    path("/add_account", addAccount, name="addAccount"),
    path("/add_rating", addRating, name="addRating"),
    path("/retrieve_account", retrieve, name="retrieve")
]