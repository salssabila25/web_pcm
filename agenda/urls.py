from django.urls import path
from . import views

app_name = "agenda"

urlpatterns = [
    path("", views.agenda_list, name="list"),
    path("<slug:slug>/", views.agenda_detail, name="detail"),
]