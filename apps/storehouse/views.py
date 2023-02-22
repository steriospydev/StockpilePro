from django.shortcuts import render
from .models import Storage, Section, Spot, Bin
# Create your views here.

def storehouse_home(request):
    return render(request, 'storehouse/storehouse_main.html', {})
