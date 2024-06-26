
from django.urls import path,include,re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    path('mpesa/donate/<int:need_id>/', views.mpesa_payment_api_view, name='mpesa-payment'),
    path('mpesa/confirm/<str:transaction_id>/', views.mpesaConfirmPaymentAPIView.as_view(), name='confirm'),
    path('checkout/<int:need_id>/', views.paypalCheckOut, name='checkout'),
    path('payment-success/<int:need_id>/', views.paypalPaymentSuccessful, name='payment-success'),
    path('payment-failed/<int:need_id>/', views.paypalpaymentFailed, name='payment-failed'),
]