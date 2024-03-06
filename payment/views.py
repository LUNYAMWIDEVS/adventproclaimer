from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from paypal.standard.ipn.views import ipn


# Create your views here.
def index(request):
    return render(request, "payment/index.html")


def room(request, room_name):
    return render(request, "payment/room.html", {"room_name": room_name})


@csrf_exempt
def paypal_ipn(request):
    ipn(request)
    return HttpResponse(status=200)
