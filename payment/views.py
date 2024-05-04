from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from paypal.standard.ipn.views import ipn


import json
from django.conf import settings
from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
# from mpesa_api.core.mpesa import Mpesa

from helpers.renderers import RequestJSONRenderer
from .tasks import perform_transaction
from .models import Payment
from needs.models import Need
from .serializers import PaymentSentSerializer
from paypal.standard.forms import PayPalPaymentsForm
import uuid
from django.urls import reverse


# Create your views here.
def index(request):
    return render(request, "payment/index.html")


def room(request, room_name):
    return render(request, "payment/room.html", {"room_name": room_name})


def paypalCheckOut(request, need_id):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        need = Need.objects.get(id=need_id)

        host = request.get_host()

        payment = Payment(
            amount=amount,
            type='C',
        )
        payment.save()
        need.received_payments.add(payment)
        need.save()
        
        paypal_checkout = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': payment.amount,
            'item_name': need.name,
            'invoice': uuid.uuid4(),
            'currency_code': 'USD',
            'notify_url': f"http://{host}{reverse('paypal-ipn')}",
            'return_url': f"http://{host}{reverse('payment-success', kwargs = {'need_id': need.id})}",
            'cancel_url': f"http://{host}{reverse('payment-failed', kwargs = {'need_id': need.id})}",
        }

        paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

        context = {
            'need': need,
            'paypal': paypal_payment
        }

        return render(request, 'payment/paypal_checkout.html', context)


def paypalPaymentSuccessful(request, need_id):

    need = Need.objects.get(id=need_id)

    return render(request, 'payment/paypal_success.html', {'need': need})

def paypalpaymentFailed(request, need_id):

    need = Need.objects.get(id=need_id)

    return render(request, 'ppayment/paypal_failed.html', {'need': need})




def mpesa_payment_api_view(request):
    """Handle Mpesa Payment"""
    if request.method == 'POST':
        # data = JSONParser().parse(request)
        payer_mobile_no = request.POST.get('mobile_no', '')
        amount = request.POST.get('amount', '')
        need_id = request.POST.get('need_id')

        # serializer = PaymentSentSerializer(data=data)
        # serializer.is_valid(raise_exception=True)
        payment = Payment(
            amount=amount,
            phone_number=payer_mobile_no,
            business_short_code=settings.MPESA_SHORT_CODE
        )

        payment.save()
        needs = Need.objects.filter(id=need_id)
        if needs.exists():
            need = needs.last()
            need.received_payments.add(payment)
            need.save()

        perform_transaction(payer_mobile_no, amount, payment.id)
    return render(request, 'payment/mpesa.html')

class mpesaPaymentAPIView(generics.GenericAPIView):
    """Handle Mpesa Payment"""
    serializer_class = PaymentSentSerializer
    renderer_classes = (RequestJSONRenderer, )
    
    def post(self, request):
        data = request.data
        payer_mobile_no = data.get('mobile_no', '')
        amount = data.get('amount', '')
        need_id = data.get('need_id')

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        payment = Payment(
            amount=amount,
            phone_number=payer_mobile_no,
            business_short_code=settings.MPESA_SHORT_CODE
        )


        payment.save()
        needs = Need.objects.filter(id=need_id)
        if needs.exists():
            need = needs.last()
            need.received_payments.add(payment)
            need.save()

        
        perform_transaction.delay(payer_mobile_no, amount, payment.id)
        return Response({"message": "Request accepted for processing"}, status=status.HTTP_201_CREATED)


class mpesaConfirmPaymentAPIView(generics.GenericAPIView):
    """Handle Mpesa Payment"""
    swagger_schema = None

    def post(self, request, transaction_id):
        """
        Handle the callback after a transaction
        """
        data = request.data
        print(data['Body'])
        try:
            payment = Payment.objects.get(id=transaction_id)
            if data['Body']['stkCallback']['ResultCode'] == 0:
                ref_number = data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
                payment.ref_number = ref_number
                payment.status = 'O'
                payment.save()
                message = "Request is processed successfully"

            else:
                payment.status = 'C'
                payment.save()
                message = data['Body']['stkCallback']['ResultDesc']
        except Exception as e:
            print(e)
            payment.status = 'C'
            payment.save()
            message = data['Body']['stkCallback']['ResultDesc']
        return Response({"message": message}, status=status.HTTP_200_OK)

