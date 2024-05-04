import requests
from celery.utils.log import get_task_logger
from django.conf import settings
from eLMS import celery_app
from .helpers import MpesaAccessToken, LipanaMpesaPpassword, MpesaC2bCredential

logger = get_task_logger(__name__)


@celery_app.task(name="check_mpesa_response")
def check_mpesa_confirmation(phone_number):
    """checks if mpesa confirmation has been returned"""
    logger.info("Checking for confirmation")
    print("\n\n\n", phone_number, '\n\n\n')
    # try:
    #     exists = Payments.objects.get(order_id=order_id)
    #     if exists:
    #         my_order = Orders.objects.get(id=order_id)
    #         my_order.status = 'S'
    #         my_order.save()
    #         return logger.info("Payment made successfully")
    # except BaseException as e:
    #     logger.info("Not yet reflected")
    #     check_mpesa_confirmation.s(order_id).apply_async(countdown=60)


@celery_app.task(name="Perform Transaction")
def perform_transaction(payer_mobile_no, amount, payment_id):
    """
    Perform Lipa na mpesa transaction
    """
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    print(api_url)
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": payer_mobile_no.split('+')[::-1][0],
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": payer_mobile_no.split('+')[::-1][0],
        "CallBackURL": f"{settings.MPESA_CALLBACK_URL}/{payment_id}/",
        "AccountReference": "Fund Test",
        "TransactionDesc": "Fund Test"
    }
    requests.post(api_url, json=request, headers=headers)


def perform_transaction_test(payer_mobile_no, amount, payment_id):
    """
    Perform Lipa na mpesa transaction
    """
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    print(api_url)
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": payer_mobile_no.split('+')[::-1][0],
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": payer_mobile_no.split('+')[::-1][0],
        "CallBackURL": f"{settings.MPESA_CALLBACK_URL}/{payment_id}/",
        "AccountReference": "Fund Test",
        "TransactionDesc": "Fund Test"
    }
    requests.post(api_url, json=request, headers=headers)
