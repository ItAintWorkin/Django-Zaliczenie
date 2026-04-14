from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        call_command("makemigrations")
        call_command("migrate")

        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin1",
                email="admin@admin.com",
                password="admin1"
            )
            print("Admin created")
        else:
            print("Admin already exists")
