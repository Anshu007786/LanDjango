from django.urls import path
from .views import calculateDistanceView

app_name = "MapApp"

urlpatterns = [
    path('',calculateDistanceView, name="calculateDistance"),
]
