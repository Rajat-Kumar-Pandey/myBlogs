from django.shortcuts import render, redirect
from .forms import RegisterForm ,UpdateProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from myBlogs.models import Blog

# Create your views here.

def signup(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect("b_index")
        
    context = {"form":form}
    return render(request, "myDude/signup.html", context)


def signin(request):
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("b_index")
        
        else:
            messages.warning(request, "Invalid credentials")
            return redirect("signin")
        
    context = {}
    return render(request, "myDude/login.html", context)

def signout(request):
    logout(request)
    return redirect("b_index")

@login_required(login_url="signin")
def profile(request):
    user = request.user
    blogs = Blog.objects.filter(user=user)
    context={"user": user, "blogs": blogs}
    return render(request, "myDude/profile.html", context)


@login_required(login_url="signin")
def update_profile(request):
    if request.user.is_authenticated:
        user = request.user
        form = UpdateProfileForm(instance=user)
        if request.method == 'POST':
            form = UpdateProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully")
                return redirect("profile")
        
    context = {"form":form}
    return render(request, "myDude/update_profile.html", context)

