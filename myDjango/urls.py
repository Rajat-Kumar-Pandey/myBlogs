# myDjango/urls.py
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from myDjango import views  # Ensure 'myDjango' is the correct project name
from myDjango.views import CustomPasswordResetView  # Import CustomPasswordResetView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('', views.home, name='home'),
    path('user/', include('myDude.urls')),
    path('myNotepad/', include('myNotepad.urls')),
    path('myBlogs/', include('myBlogs.urls')),
    path('fatafat/', include('fatafat_money.urls')),  # Added trailing slash
    
    # Development tools (optional, for development purposes)
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
