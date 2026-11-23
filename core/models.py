from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class OrganizationProfile(TimeStampedModel):
    nama = models.CharField("Nama PCM", max_length=150, default="Pimpinan Cabang Muhammadiyah")
    nama_singkat = models.CharField(max_length=50, blank=True)
    tagline = models.CharField(max_length=200, blank=True)
    tentang = models.TextField(blank=True)
    jumlah_anggota = models.PositiveIntegerField("Jumlah anggota ber-KTAM", default=0)
    gambar_hero = models.ImageField(upload_to="organization/", blank=True, null=True)
    kecamatan = models.CharField(max_length=100, blank=True)
    kabupaten = models.CharField("Kabupaten/Kota", max_length=100, blank=True)
    provinsi = models.CharField(max_length=100, blank=True)
    alamat = models.TextField(blank=True)
    telepon = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    jam_kantor = models.CharField(max_length=120, blank=True)
    logo = models.ImageField(upload_to="organization/", blank=True, null=True)
    sejarah = models.TextField(blank=True)
    visi = models.TextField(blank=True)
    misi = models.TextField(blank=True)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    maps_embed = models.URLField("URL embed Google Maps", blank=True)

    class Meta:
        verbose_name = "Profil Organisasi"
        verbose_name_plural = "Profil Organisasi"

    def __str__(self):
        return self.nama

    def save(self, *args, **kwargs):
        self.pk = 1

        if self._state.adding:
            existing = type(self).objects.filter(pk=1).only("created_at").first()
            if existing:
                self.created_at = existing.created_at

        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def wilayah(self):
        parts = [p for p in [self.kecamatan, self.kabupaten, self.provinsi] if p]
        return ", ".join(parts)



class Division(TimeStampedModel):
    JENIS = [
        ("majelis", "Majelis"),
        ("bidang", "Bidang"),
        ("lembaga", "Lembaga"),
        ("ortom", "Ortom"),
    ]
    nama = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    jenis = models.CharField(max_length=20, choices=JENIS, default="majelis")
    deskripsi = models.TextField(blank=True)
    urutan = models.PositiveIntegerField(default=0)
    aktif = models.BooleanField(default=True)

    class Meta:
        ordering = ["urutan", "nama"]
        verbose_name = "Majelis/Bidang"
        verbose_name_plural = "Majelis/Bidang"

    def __str__(self):
        return self.nama

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)


class Management(TimeStampedModel):
    nama = models.CharField("Nama lengkap", max_length=150)
    jabatan = models.CharField(max_length=120)
    division = models.ForeignKey(
        Division, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="pengurus", verbose_name="Majelis/Bidang",
    )
    periode = models.CharField(max_length=30, blank=True, help_text="Contoh: 2022–2027")
    foto = models.ImageField(upload_to="management/", blank=True, null=True)
    urutan = models.PositiveIntegerField(default=0)
    aktif = models.BooleanField(default=True)

    class Meta:
        ordering = ["urutan", "nama"]
        verbose_name = "Pengurus"
        verbose_name_plural = "Pengurus"

    def __str__(self):
        return f"{self.nama} — {self.jabatan}"


phone_validator = RegexValidator(
    regex=r"^[0-9+\-\s]{9,20}$",
    message="Nomor telepon hanya boleh angka, +, -, dan spasi (9–20 karakter).",
)

class Ranting(TimeStampedModel):
    nama = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    alamat = models.TextField(blank=True)
    desa_kelurahan = models.CharField(max_length=120, blank=True)
    kecamatan = models.CharField(max_length=120, blank=True)
    ketua = models.CharField(max_length=120, blank=True)
    telepon = models.CharField(
        max_length=20, blank=True, validators=[phone_validator]
    )
    email = models.EmailField(blank=True)
    deskripsi = models.TextField(blank=True)
    foto = models.ImageField(upload_to="ranting/", blank=True)
    urutan = models.PositiveIntegerField(default=0)
    aktif = models.BooleanField(default=True)

    class Meta:
        ordering = ["urutan", "nama"]
        verbose_name = "Ranting"
        verbose_name_plural = "Ranting"

    def __str__(self):
        return self.nama


class AmalUsaha(TimeStampedModel):
    JENIS = [
        ("pendidikan", "Pendidikan"),
        ("kesehatan", "Kesehatan"),
        ("sosial", "Sosial / Panti"),
        ("ekonomi", "Ekonomi"),
        ("dakwah", "Dakwah / Masjid"),
        ("lainnya", "Lainnya"),
    ]

    nama = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    jenis = models.CharField(max_length=20, choices=JENIS, default="lainnya")
    ranting = models.ForeignKey(
        Ranting,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="amal_usaha",
    )
    alamat = models.TextField(blank=True)
    pimpinan = models.CharField(max_length=120, blank=True)
    telepon = models.CharField(
        max_length=20, blank=True, validators=[phone_validator]
    )
    deskripsi = models.TextField(blank=True)
    foto = models.ImageField(upload_to="amal_usaha/", blank=True)
    urutan = models.PositiveIntegerField(default=0)
    aktif = models.BooleanField(default=True)

    class Meta:
        ordering = ["jenis", "urutan", "nama"]
        verbose_name = "Amal Usaha"
        verbose_name_plural = "Amal Usaha"

    def __str__(self):
        return self.nama


class ContactMessage(TimeStampedModel):
    STATUS = [
        ("baru", "Baru"),
        ("dibaca", "Dibaca"),
        ("ditindaklanjuti", "Ditindaklanjuti"),
        ("diarsipkan", "Diarsipkan"),
    ]
    nama = models.CharField(max_length=120)
    email = models.EmailField()
    telepon = models.CharField(max_length=20, blank=True, validators=[phone_validator])
    subjek = models.CharField(max_length=150)
    pesan = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default="baru")
    catatan_admin = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Pesan Masyarakat"
        verbose_name_plural = "Pesan Masyarakat"

    def __str__(self):
        return f"{self.subjek} — {self.nama}"