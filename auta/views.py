from django.shortcuts import render, get_object_or_404
from .models import Vyrobce, VyrobniZavod, Auto

def vyrobce_list(request):
    vyrobci = Vyrobce.objects.all()
    return render(request, 'vyrobce_list.html', {'vyrobci': vyrobci})

def zavod_list(request):
    zavody = VyrobniZavod.objects.all()
    return render(request, 'zavod_list.html', {'zavody': zavody})

def auto_list(request):
    auta = Auto.objects.all()
    return render(request, 'auto_list.html', {'auta': auta})

def auto_detail(request, id):
    auto = get_object_or_404(Auto, id=id)
    return render(request, 'auto_detail.html', {'auto': auto})

def index(request):
    return render(request, 'index.html')
