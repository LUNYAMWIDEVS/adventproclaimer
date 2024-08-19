from django.urls import path
from . import views

urlpatterns = [
    path('bibleworker/', views.bible_worker_daily_report_list, name='bible_worker_daily_report_list'),
    path('bibleworker/create/', views.bible_worker_daily_report_create, name='bible_worker_daily_report_create'),
    path('bibleworker/update/<int:pk>/', views.bible_worker_daily_report_update, name='bible_worker_daily_report_update'),
    path('bibleworker/delete/<int:pk>/', views.bible_worker_daily_report_delete, name='bible_worker_daily_report_delete'),
    path('medicalmissionary/', views.medical_missionary_daily_report_list, name='medical_missionary_daily_report_list'),
    path('medicalmissionary/create/', views.medical_missionary_daily_report_create, name='medical_missionary_daily_report_create'),
    path('medicalmissionary/update/<int:pk>/', views.medical_missionary_daily_report_update, name='medical_missionary_daily_report_update'),
    path('medicalmissionary/delete/<int:pk>/', views.medical_missionary_daily_report_delete, name='medical_missionary_daily_report_delete'),
]
