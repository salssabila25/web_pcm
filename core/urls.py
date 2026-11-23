from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("profil/", views.profile, name="profile"),
    path("kontak/", views.contact, name="contact"),
]