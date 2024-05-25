from django.shortcuts import render
from .models import ocr_data

def home(request):
    return render(request, 'home.html')

def show_data(request):
    data = ocr_data.objects.all()
    return render(request, 'show_data.html', {'data': data})
