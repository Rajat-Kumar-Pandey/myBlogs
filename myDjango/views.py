from django.http import HttpResponse
from django.shortcuts import render 

from django.contrib.auth.views import PasswordResetView
from .forms import CustomPasswordResetForm
def home(request):
    return render(request, 'website/index.html')
    
    

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm



# return render(request, 'index.html')