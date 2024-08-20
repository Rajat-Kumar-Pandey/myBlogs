from django.urls import path, include
# Uncomment the following line if you plan to use the admin site
# from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views  # Ensure 'myDjango' is the correct app name

urlpatterns = [
    path("", views.myGpt, name="myGpt"),

    # Development tools (optional, for development purposes)
    # path("__reload__/", include("django_browser_reload.urls")),
]
