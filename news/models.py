from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NewsCategory(TimeStampedModel):
    nama = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    deskripsi = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["nama"]
        verbose_name = "Kategori Berita"
        verbose_name_plural = "Kategori Berita"

    def __str__(self):
        return self.nama

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            status="published", published_at__lte=timezone.now()
        )


class News(TimeStampedModel):
    STATUS = [("draft", "Draft"), ("published", "Published"), ("archived", "Archived")]

    judul = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    kategori = models.ForeignKey(
        NewsCategory, on_delete=models.PROTECT, related_name="berita", verbose_name="Kategori"
    )
    penulis = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="berita", verbose_name="Penulis",
    )
    ringkasan = models.CharField(max_length=300, blank=True)
    isi = models.TextField()
    gambar = models.ImageField(upload_to="news/%Y/%m/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default="draft")
    published_at = models.DateTimeField("Tanggal publikasi", null=True, blank=True)
    unggulan = models.BooleanField(default=False, help_text="Tampilkan di beranda")

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name = "Berita"
        verbose_name_plural = "Berita"

    def __str__(self):
        return self.judul

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.judul) or "berita"
            slug = base
            n = 2
            while News.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        if self.status == "published" and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("news:detail", kwargs={"slug": self.slug})