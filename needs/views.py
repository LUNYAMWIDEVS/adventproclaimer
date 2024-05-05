from django.shortcuts import render
from .models import Need

# Create your views here.
def index(request):
    needs = Need.objects.all()
    context = {
        "needs":needs
    }
    return render(request,"needs/index.html",context)