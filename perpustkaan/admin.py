from django.contrib import admin
from .models import Buku, Siswa, Peminjaman


@admin.register(Buku)
class BukuAdmin(admin.ModelAdmin):
    list_display = ('id', 'judul', 'pengarang', 'kategori', 'penerbit', 'tahun_terbit', 'rak', 'stok')
    search_fields = ('judul', 'pengarang', 'penerbit')
    list_filter = ('kategori',)


@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama', 'kelas', 'nis')
    search_fields = ('nama', 'nis')
    list_filter = ('kelas',)


@admin.register(Peminjaman)
class PeminjamanAdmin(admin.ModelAdmin):
    list_display = ('id', 'siswa', 'buku', 'tanggal_pinjam', 'jatuh_tempo', 'status')
    search_fields = ('siswa__nama', 'buku__judul')
    list_filter = ('status',)
