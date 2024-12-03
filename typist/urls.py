from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.typing_test, name='typing_test'),
]