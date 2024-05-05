from django.urls import path
from . import views

urlpatterns = [
    path("needs/",views.index,name="needs")
]