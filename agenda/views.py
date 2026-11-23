from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Agenda


def agenda_list(request):
    now = timezone.now()
    status = request.GET.get("status", "akan")
    qs = Agenda.objects.filter(status_publikasi="published").select_related("penyelenggara")
    if status == "selesai":
        qs = qs.filter(tanggal_mulai__lt=now).order_by("-tanggal_mulai")
    else:
        qs = qs.filter(tanggal_mulai__gte=now).order_by("tanggal_mulai")
    paginator = Paginator(qs, 8)
    page = paginator.get_page(request.GET.get("page"))
    return render(request, "agenda/agenda_list.html", {
        "page_obj": page,
        "status": status,
        "jumlah_akan": Agenda.objects.filter(status_publikasi="published", tanggal_mulai__gte=now).count(),
        "jumlah_selesai": Agenda.objects.filter(status_publikasi="published", tanggal_mulai__lt=now).count(),
    })


def agenda_detail(request, slug):
    agenda = get_object_or_404(
        Agenda.objects.filter(status_publikasi="published").select_related("penyelenggara"),
        slug=slug,
    )
    return render(request, "agenda/agenda_detail.html", {"agenda": agenda})