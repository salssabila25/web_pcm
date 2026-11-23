from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone

from agenda.models import Agenda
from news.models import News

from .forms import ContactForm
from .models import Division, Management, OrganizationProfile, Ranting, AmalUsaha


def home(request):
    now = timezone.now()
    berita = News.published.select_related("kategori", "penulis").order_by("-published_at")[:3]
    agenda = (
        Agenda.objects.filter(status_publikasi="published", tanggal_mulai__gte=now)
        .select_related("penyelenggara")
        .order_by("tanggal_mulai")[:3]
    )
    return render(request, "core/home.html", {
        "berita": berita,
        "agenda": agenda,
        "divisions": Division.objects.filter(aktif=True)[:6],
        "jumlah_pengurus": Management.objects.filter(aktif=True).count(),
        "jumlah_bidang": Division.objects.filter(aktif=True).count(),
    })


def profile(request):
    org = OrganizationProfile.load()
    divisions = Division.objects.filter(aktif=True)
    groups = [
        {"division": d, "members": list(d.pengurus.filter(aktif=True))}
        for d in divisions
    ]
    leaders = Management.objects.filter(aktif=True, division__isnull=True)
    return render(request, "core/profile.html", {
        "org": org,
        "groups": groups,
        "leaders": leaders,
        "ranting_list": Ranting.objects.filter(aktif=True).order_by("urutan", "nama"),
        "amal_usaha_list": AmalUsaha.objects.filter(aktif=True).select_related("ranting").order_by("nama"),
    })


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pesan Anda berhasil dikirim. Terima kasih telah menghubungi PCM.")
            return redirect("core:contact")
        messages.error(request, "Pesan belum terkirim. Periksa kembali isian Anda.")
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})