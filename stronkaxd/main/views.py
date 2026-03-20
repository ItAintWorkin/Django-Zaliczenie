from django.shortcuts import render , HttpResponse
from qrgenerator.qrtoimg import get_base64

# Create your views here.
def home(request):
    return render(request, "base.html")

def generator(request):

    text = request.GET.get('text', 'https://youtu.be/dQw4w9WgXcQ')
    context = {}
    try:
        context['img'] = get_base64(text)

    except Exception as e:
        context['error'] = e

    return render(request, "generator.html", context)

def yourqr(request):
    return render(request, "yourqr.html")

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")