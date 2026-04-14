from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class QRCode_save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.TextField()
    image_base64 = models.TextField()