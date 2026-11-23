from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import News, NewsCategory


def news_list(request, category_slug=None):
    qs = News.published.select_related("kategori", "penulis")
    kategori_aktif = None
    if category_slug:
        kategori_aktif = get_object_or_404(NewsCategory, slug=category_slug)
        qs = qs.filter(kategori=kategori_aktif)
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(judul__icontains=q) | Q(ringkasan__icontains=q) | Q(isi__icontains=q))
    paginator = Paginator(qs, 9)
    page = paginator.get_page(request.GET.get("page"))
    return render(request, "news/news_list.html", {
        "page_obj": page,
        "categories": NewsCategory.objects.all(),
        "kategori_aktif": kategori_aktif,
        "q": q,
    })


def news_detail(request, slug):
    berita = get_object_or_404(
        News.published.select_related("kategori", "penulis"), slug=slug
    )
    terkait = News.published.filter(kategori=berita.kategori).exclude(pk=berita.pk)[:3]
    return render(request, "news/news_detail.html", {"berita": berita, "terkait": terkait})