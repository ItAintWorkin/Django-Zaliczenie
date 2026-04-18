from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import QRCode_save
import traceback

import qrgenerator.export as export
from qrgenerator.qrcode import QRCode


# Create your views here.
def home(request):
    return render(request, "base.html")

def generator(request):

    text = request.GET.get('text', 'https://youtu.be/dQw4w9WgXcQ')
    context = {}
    try:
        qr = QRCode()
        qr["data"] = text
        qr.update_matrix()
        context['img'] = export.as_jpg_base64(qr)

    except Exception as e:
        context['error'] = e
        print(traceback.format_exc())

    return render(request, "generator.html", context)

def yourqr(request):

    if not request.user.is_authenticated:
        return render(request, "yourqr.html")
    
    qrs = QRCode_save.objects.filter(user=request.user).order_by('-id')
    return render(request, "yourqr.html", {"qrs": qrs})

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
            messages.error(request, "User not found ¯\_(ツ)_/¯")

    return render(request, "login.html")

def logout_view(request):
    auth_logout(request)
    return redirect("home")

@login_required
def save_qr(request):
    if request.method == "POST":
        QRCode_save.objects.create(
            user=request.user,
            data=request.POST.get("text"),
            image_base64=request.POST.get("img")
        )

    return redirect(f"/generator?text={request.POST.get('text')}")

@login_required
def delete_qr(request, qr_id):
    qr = get_object_or_404(QRCode_save, id=qr_id, user=request.user)
    qr.delete()
    return redirect("yourqr")

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def all_qrs(request):
    qrs = QRCode_save.objects.all().order_by('-id')
    return render(request, "all_qrs.html", {"qrs": qrs})

@user_passes_test(is_admin)
def admin_delete_qr(request, qr_id):
    qr = get_object_or_404(QRCode_save, id=qr_id)
    qr.delete()
    return redirect("all_qrs")

@user_passes_test(is_admin)
def admin_delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user == user:
        return redirect("all_qrs")
    
    user.delete()
    return redirect("all_qrs")
