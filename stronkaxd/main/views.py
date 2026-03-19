from django.shortcuts import render , HttpResponse

# Create your views here.
def home(request):
    return render(request, "base.html")

def generator(request):
    return render(request, "generator.html")

def yourqr(request):
    return render(request, "yourqr.html")

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")