from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout

import qrgenerator.export as export
from qrgenerator.qrcode import QRCode


# Create your views here.
def home(request):
    return render(request, "base.html")

def generator(request):

    text = request.GET.get('text', 'https://youtu.be/dQw4w9WgXcQ')
    context = {}
    try:
        context['img'] = export.as_jpg_base64(QRCode(text))

    except Exception as e:
        context['error'] = e

    return render(request, "generator.html", context)

def yourqr(request):
    return render(request, "yourqr.html")

def debug(request):
    return render(request, "debug.html")

def register(request):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        repeat_password = request.POST.get("repeat-password")

        if password != repeat_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, "Account created successfully! You can now log in.")
        return redirect("login")

    return render(request, "register.html")

def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  
        else:
            messages.error(request, "User not found")

    return render(request, "login.html")

def logout_view(request):
    auth_logout(request)
    return redirect("home")