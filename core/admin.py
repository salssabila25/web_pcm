from django.contrib import admin

from .models import (
    AmalUsaha,
    ContactMessage,
    Division,
    Management,
    OrganizationProfile,
    Ranting,
)

admin.site.site_header = "Administrasi Website PCM"
admin.site.site_title = "Admin PCM"
admin.site.index_title = "Dashboard Pengelolaan Konten"


@admin.register(OrganizationProfile)
class OrganizationProfileAdmin(admin.ModelAdmin):
    list_display = ("nama", "kecamatan", "kabupaten", "updated_at")
    fieldsets = (
        ("Identitas", {
            "fields": (
                "nama", "nama_singkat", "tagline",
                "kecamatan", "kabupaten", "provinsi",
                "logo", "gambar_hero",
            ),
        }),
        ("Tentang Organisasi", {
            "fields": ("tentang", "jumlah_anggota"),
        }),
        ("Kontak", {
            "fields": ("alamat", "telepon", "email", "jam_kantor", "maps_embed"),
        }),
        ("Sosial Media", {
            "fields": ("instagram", "facebook", "youtube"),
        }),
        ("Konten Profil", {
            "fields": ("sejarah", "visi", "misi"),
        }),
    )


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ("nama", "jenis", "urutan", "aktif")
    list_filter = ("jenis", "aktif")
    search_fields = ("nama",)
    prepopulated_fields = {"slug": ("nama",)}


@admin.register(Management)
class ManagementAdmin(admin.ModelAdmin):
    list_display = ("nama", "jabatan", "division", "periode", "urutan", "aktif")
    list_filter = ("aktif", "division")
    search_fields = ("nama", "jabatan")
    list_editable = ("urutan", "aktif")


@admin.register(Ranting)
class RantingAdmin(admin.ModelAdmin):
    list_display = ("nama", "kecamatan", "ketua", "aktif")
    list_filter = ("aktif", "kecamatan")
    search_fields = ("nama", "ketua", "kecamatan")
    prepopulated_fields = {"slug": ("nama",)}


@admin.register(AmalUsaha)
class AmalUsahaAdmin(admin.ModelAdmin):
    list_display = ("nama", "jenis", "ranting", "aktif")
    list_filter = ("jenis", "ranting", "aktif")
    search_fields = ("nama", "pimpinan")
    prepopulated_fields = {"slug": ("nama",)}


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("subjek", "nama", "email", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("nama", "email", "subjek", "pesan")
    readonly_fields = ("nama", "email", "telepon", "subjek", "pesan", "created_at", "updated_at")
    list_editable = ("status",)
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False
