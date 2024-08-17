# fatafat_money/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('f_index/', views.index, name='f_index'),  # Added trailing slash for consistency
]
