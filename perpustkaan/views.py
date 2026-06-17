from django.shortcuts import render, redirect
from django.http import Http404
from django.db import connection
from .models import Buku, Siswa, Peminjaman

# Ambil nama tabel asli dari database secara dinamis
TABEL_BUKU = Buku._meta.db_table
TABEL_SISWA = Siswa._meta.db_table
TABEL_PEMINJAMAN = Peminjaman._meta.db_table


# ─── HELPER ───────────────────────────────────────────────────
def get_raw_object_or_404(model, pk, table_name):
    query = f"SELECT * FROM {table_name} WHERE id = %s"
    objects = list(model.objects.raw(query, [pk]))
    if not objects:
        raise Http404(f"{model.name} tidak ditemukan")
    return objects[0]


# ─── BUKU VIEWS ────────────────────────────────────────────────

def dashboard(request):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT COUNT(*) FROM {TABEL_BUKU}")
        total_buku = cursor.fetchone()[0]

        cursor.execute(f"SELECT COUNT(*) FROM {TABEL_SISWA}")
        total_siswa = cursor.fetchone()[0]

        cursor.execute(f"SELECT COUNT(*) FROM {TABEL_PEMINJAMAN}")
        total_peminjaman = cursor.fetchone()[0]

        cursor.execute(f"SELECT COUNT(*) FROM {TABEL_PEMINJAMAN} WHERE status = %s", ['Dipinjam'])
        peminjaman_aktif = cursor.fetchone()[0]

    return render(request, 'perpustakaan/dashboard.html', {
        'total_buku': total_buku,
        'total_siswa': total_siswa,
        'total_peminjaman': total_peminjaman,
        'peminjaman_aktif': peminjaman_aktif,
    })


def buku_list(request):
    buku_list = Buku.objects.raw(f"SELECT * FROM {TABEL_BUKU}")
    return render(request, 'buku/list.html', {'buku_list': buku_list})


def buku_tambah(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute(f"""
                INSERT INTO {TABEL_BUKU} (judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, [
                request.POST['judul'],
                request.POST['pengarang'],
                request.POST['kategori'],
                request.POST['penerbit'],
                request.POST['tahun_terbit'],
                request.POST['rak'],
                request.POST['stok'],
                request.POST.get('deskripsi', '')
            ])
        return redirect('buku_list')
    return render(request, 'buku/tambah.html')


def buku_detail(request, pk):
    buku = get_raw_object_or_404(Buku, pk, TABEL_BUKU)
    return render(request, 'buku/detail.html', {'buku': buku})


def buku_edit(request, pk):
    buku = get_raw_object_or_404(Buku, pk, TABEL_BUKU)
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute(f"""
                UPDATE {TABEL_BUKU} 
                SET judul = %s, pengarang = %s, kategori = %s, penerbit = %s, 
                    tahun_terbit = %s, rak = %s, stok = %s, deskripsi = %s
                WHERE id = %s
            """, [
                request.POST['judul'],
                request.POST['pengarang'],
                request.POST['kategori'],
                request.POST['penerbit'],
                request.POST['tahun_terbit'],
                request.POST['rak'],
                request.POST['stok'],
                request.POST.get('deskripsi', ''),
                pk
            ])
        return redirect('buku_list')
    return render(request, 'buku/edit.html', {'buku': buku})


def buku_delete(request, pk):
    buku = get_raw_object_or_404(Buku, pk, TABEL_BUKU)
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM {TABEL_BUKU} WHERE id = %s", [pk])
        return redirect('buku_list')
    return render(request, 'buku/delete.html', {'buku': buku})


# ─── SISWA VIEWS ───────────────────────────────────────────────

def siswa_list(request):
    siswa_list = Siswa.objects.raw(f"SELECT * FROM {TABEL_SISWA}")
    return render(request, 'siswa/list-siswa.html', {'siswa_list': siswa_list})
def siswa_tambah(request):
    if request.method == 'POST':
        # Menggunakan 1 atau 0 agar aman di semua database (SQLite/MySQL/Postgres)
        is_active = 1 if request.POST.get('is_active', 'true') == 'true' else 0
        with connection.cursor() as cursor:
            cursor.execute(f"""
                INSERT INTO {TABEL_SISWA} (nama, kelas, nis, is_active)
                VALUES (%s, %s, %s, %s)
            """, [
                request.POST['nama'],
                request.POST['kelas'],
                request.POST['nis'],
                is_active
            ])
        return redirect('siswa_list')
    return render(request, 'siswa/tambah-siswa.html')


def siswa_detail(request, pk):
    siswa = get_raw_object_or_404(Siswa, pk, TABEL_SISWA)
    
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT COUNT(*) FROM {TABEL_PEMINJAMAN} WHERE siswa_id = %s", [pk])
        total_peminjaman = cursor.fetchone()[0]

        cursor.execute(f"SELECT COUNT(*) FROM {TABEL_PEMINJAMAN} WHERE siswa_id = %s AND status = %s", [pk, 'Dipinjam'])
        peminjaman_aktif_count = cursor.fetchone()[0]

    return render(request, 'siswa/detail-siswa.html', {
        'siswa': siswa,
        'total_peminjaman': total_peminjaman,
        'peminjaman_aktif_count': peminjaman_aktif_count,
    })


def siswa_edit(request, pk):
    siswa = get_raw_object_or_404(Siswa, pk, TABEL_SISWA)
    if request.method == 'POST':
        is_active = 1 if request.POST.get('is_active', 'true') == 'true' else 0
        with connection.cursor() as cursor:
            cursor.execute(f"""
                UPDATE {TABEL_SISWA} 
                SET nama = %s, kelas = %s, nis = %s, is_active = %s
                WHERE id = %s
            """, [
                request.POST['nama'],
                request.POST['kelas'],
                request.POST['nis'],
                is_active,
                pk
            ])
        return redirect('siswa_list')
    return render(request, 'siswa/edit-siswa.html', {'siswa': siswa})


def siswa_hapus(request, pk):
    siswa = get_raw_object_or_404(Siswa, pk, TABEL_SISWA)
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM {TABEL_SISWA} WHERE id = %s", [pk])
        return redirect('siswa_list')
    return render(request, 'siswa/hapus-siswa.html', {'siswa': siswa})


# ─── PEMINJAMAN VIEWS ─────────────────────────────────────────

def peminjaman_list(request):
    peminjaman_list = Peminjaman.objects.raw(f"SELECT * FROM {TABEL_PEMINJAMAN}")
    return render(request, 'peminjaman/list-peminjaman.html', {'peminjaman_list': peminjaman_list})

def peminjaman_tambah(request):
    if request.method == 'POST':
        siswa_id = request.POST['siswa_id']
        buku_id = request.POST['buku_id']
        
        get_raw_object_or_404(Siswa, siswa_id, TABEL_SISWA)
        get_raw_object_or_404(Buku, buku_id, TABEL_BUKU)

        with connection.cursor() as cursor:
            cursor.execute(f"""
                UPDATE {TABEL_BUKU} 
                SET stok = stok - 1 
                WHERE id = %s AND stok > 0
            """, [buku_id])
            
            cursor.execute(f"""
                INSERT INTO {TABEL_PEMINJAMAN} (siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, catatan, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, [
                siswa_id,
                buku_id,
                request.POST['tanggal_pinjam'],
                request.POST['jatuh_tempo'],
                request.POST.get('keperluan', ''),
                request.POST.get('catatan', ''),
                'Dipinjam'
            ])
            
        return redirect('peminjaman_list')

    siswa_list = Siswa.objects.raw(f"SELECT * FROM {TABEL_SISWA} WHERE is_active = 1")
    buku_list = Buku.objects.raw(f"SELECT * FROM {TABEL_BUKU} WHERE stok > 0")
    
    return render(request, 'peminjaman/tambah-peminjaman.html', {
        'siswa_list': siswa_list,
        'buku_list': buku_list,
    })
def peminjaman_ubah_status(request, pk):
    peminjaman = get_raw_object_or_404(Peminjaman, pk, TABEL_PEMINJAMAN)
    
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute(f"""
                UPDATE {TABEL_PEMINJAMAN} 
                SET status = 'Dikembalikan' 
                WHERE id = %s
            """, [pk])

            cursor.execute(f"""
                UPDATE {TABEL_BUKU} 
                SET stok = stok + 1 
                WHERE id = (SELECT buku_id FROM {TABEL_PEMINJAMAN} WHERE id = %s)
            """, [pk])

        return redirect('peminjaman_list')
        
    return render(request, 'peminjaman/ubah-status.html', {'peminjaman': peminjaman})