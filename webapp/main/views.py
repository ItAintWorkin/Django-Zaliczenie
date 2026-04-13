from django.shortcuts import render

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

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")