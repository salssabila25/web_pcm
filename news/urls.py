from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    path("", views.news_list, name="list"),
    path("kategori/<slug:category_slug>/", views.news_list, name="category"),
    path("<slug:slug>/", views.news_detail, name="detail"),
]