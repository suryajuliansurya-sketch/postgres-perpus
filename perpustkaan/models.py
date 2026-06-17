from django.db import models


class Buku(models.Model):
    KATEGORI_CHOICES = [
        ('Novel', 'Novel'),
        ('Sejarah', 'Sejarah'),
        ('Pendidikan', 'Pendidikan'),
    ]

    judul = models.CharField(max_length=200)
    pengarang = models.CharField(max_length=150)
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES)
    penerbit = models.CharField(max_length=150)
    tahun_terbit = models.PositiveIntegerField()
    rak = models.CharField(max_length=20)
    stok = models.PositiveIntegerField(default=0)
    deskripsi = models.TextField(blank=True, default='')

    class Meta:
        verbose_name = 'Buku'
        verbose_name_plural = 'Buku'
        ordering = ['-id']

    def __str__(self):
        return self.judul


class Siswa(models.Model):
    nama = models.CharField(max_length=150)
    kelas = models.CharField(max_length=50)
    nis = models.CharField(max_length=20, unique=True, verbose_name='NIS')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Siswa'
        verbose_name_plural = 'Siswa'
        ordering = ['-id']

    def __str__(self):
        return f"{self.nama} ({self.nis})"


class Peminjaman(models.Model):
    STATUS_CHOICES = [
        ('Dipinjam', 'Dipinjam'),
        ('Dikembalikan', 'Dikembalikan'),
        ('Terlambat', 'Terlambat'),
    ]

    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, related_name='peminjaman')
    buku = models.ForeignKey(Buku, on_delete=models.CASCADE, related_name='peminjaman')
    tanggal_pinjam = models.DateField()
    jatuh_tempo = models.DateField()
    keperluan = models.CharField(max_length=100, blank=True, default='')
    catatan = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Dipinjam')

    class Meta:
        verbose_name = 'Peminjaman'
        verbose_name_plural = 'Peminjaman'
        ordering = ['-id']

    def __str__(self):
        return f"{self.siswa.nama} - {self.buku.judul}"
