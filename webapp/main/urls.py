from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("generator", views.generator, name = "generator"),
    path("yourqr", views.yourqr, name = "yourqr"),
    path("debug", views.debug, name = "debug"),
    path("login", views.login_view, name = "login"),
    path("register", views.register, name = "register"),
    path("logout", views.logout_view, name="logout"),
    path("save_qr", views.save_qr, name="save_qr"),
    path("delete_qr/<int:qr_id>", views.delete_qr, name="delete_qr"),
    path("all_qrs", views.all_qrs, name="all_qrs"),
    path("admin_delete_qr/<int:qr_id>", views.admin_delete_qr, name="admin_delete_qr"),
    path("admin_delete_user/<int:user_id>", views.admin_delete_user, name="admin_delete_user")
]