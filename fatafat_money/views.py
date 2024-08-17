# fatafat_money/views.py
from django.shortcuts import render

def index(request):
    return render(request, 'fatafat_money/index.html')
