from django.contrib import admin

from .models import Agenda


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = (
        "judul",
        "tanggal_mulai",
        "lokasi",
        "penyelenggara",
        "status_publikasi",
        "get_label_status",
    )
    list_filter = ("status_publikasi", "tanggal_mulai", "penyelenggara")
    search_fields = ("judul", "deskripsi", "lokasi")
    prepopulated_fields = {"slug": ("judul",)}
    date_hierarchy = "tanggal_mulai"

    @admin.display(description="Status Kegiatan")
    def get_label_status(self, obj):
        return obj.label_status