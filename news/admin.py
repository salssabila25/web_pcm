from django.contrib import admin

from .models import News, NewsCategory


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ("nama", "slug", "created_at")
    prepopulated_fields = {"slug": ("nama",)}
    search_fields = ("nama",)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("judul", "kategori", "penulis", "status", "published_at", "unggulan")
    list_filter = ("status", "kategori", "unggulan", "published_at")
    search_fields = ("judul", "ringkasan", "isi")
    prepopulated_fields = {"slug": ("judul",)}
    list_editable = ("status", "unggulan")
    date_hierarchy = "published_at"
    autocomplete_fields = ("kategori",)
    fieldsets = (
        (None, {"fields": ("judul", "slug", "kategori", "penulis", "ringkasan", "isi", "gambar")}),
        ("Publikasi", {"fields": ("status", "published_at", "unggulan")}),
    )

    def save_model(self, request, obj, form, change):
        if not obj.penulis_id:
            obj.penulis = request.user
        if obj.status == "published" and not obj.published_at:
            from django.utils import timezone
            obj.published_at = timezone.now()
        super().save_model(request, obj, form, change)