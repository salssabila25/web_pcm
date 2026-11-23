from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Agenda(TimeStampedModel):
    STATUS = [("draft", "Draft"), ("published", "Published")]

    judul = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    deskripsi = models.TextField()
    lokasi = models.CharField(max_length=200)
    tanggal_mulai = models.DateTimeField()
    tanggal_selesai = models.DateTimeField(null=True, blank=True)
    penyelenggara = models.ForeignKey(
        "core.Division", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="agenda", verbose_name="Penyelenggara",
    )
    poster = models.ImageField(upload_to="agenda/%Y/%m/", blank=True, null=True)
    status_publikasi = models.CharField(max_length=20, choices=STATUS, default="draft")

    class Meta:
        ordering = ["tanggal_mulai"]
        verbose_name = "Agenda"
        verbose_name_plural = "Agenda"

    def __str__(self):
        return self.judul

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.judul) or "agenda"
            slug = base
            n = 2
            while Agenda.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("agenda:detail", kwargs={"slug": self.slug})

    @property
    def status_kegiatan(self):
        now = timezone.now()
        if now < self.tanggal_mulai:
            return "akan_datang"
        if self.tanggal_selesai and now > self.tanggal_selesai:
            return "selesai"
        if not self.tanggal_selesai and now.date() > self.tanggal_mulai.date():
            return "selesai"
        return "berlangsung"

    @property
    def label_status(self):
        return {
            "akan_datang": "Akan Datang",
            "berlangsung": "Berlangsung",
            "selesai": "Sudah Terlaksana",
        }[self.status_kegiatan]

    @property
    def is_upcoming(self):
        return self.status_kegiatan in ("akan_datang", "berlangsung")