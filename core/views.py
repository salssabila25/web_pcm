import re

from django.contrib import messages
from django.db.models import Prefetch
from django.shortcuts import redirect, render
from django.utils import timezone

from agenda.models import Agenda
from news.models import News

from .forms import ContactForm
from .models import Division, Management, OrganizationProfile, Ranting, AmalUsaha


def _management_order(person):
    title = person.jabatan.casefold()
    if "wakil ketua" in title:
        priority = 10
    elif "sekretaris" in title:
        priority = 30 if "wakil" in title else 20
    elif "bendahara" in title:
        priority = 50 if "wakil" in title else 40
    else:
        priority = 60

    number = re.search(r"\d+", title)
    return (
        priority,
        int(number.group()) if number else 0,
        person.urutan,
        person.nama.casefold(),
    )


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
    unassigned_management = list(
        Management.objects.filter(aktif=True, division__isnull=True)
    )
    chair = next(
        (
            person for person in unassigned_management
            if person.jabatan.casefold().strip() in {"ketua", "ketua pcm"}
            or person.jabatan.casefold().strip().startswith(
                ("ketua pcm ", "ketua pimpinan cabang")
            )
        ),
        None,
    )
    board = [
        person for person in unassigned_management
        if person is not chair and "anggota" not in person.jabatan.casefold()
    ]
    board.sort(key=_management_order)
    members = [
        person for person in unassigned_management
        if "anggota" in person.jabatan.casefold()
    ]

    divisions = Division.objects.filter(aktif=True).prefetch_related(
        Prefetch("pengurus", queryset=Management.objects.filter(aktif=True))
    )
    groups = []
    for division in divisions:
        division_members = list(division.pengurus.all())
        if division_members:
            groups.append({"division": division, "members": division_members})

    return render(request, "core/profile.html", {
        "org": org,
        "chair": chair,
        "board": board,
        "members": members,
        "groups": groups,
        "multiple_teams": len(groups) + bool(members) > 1,
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