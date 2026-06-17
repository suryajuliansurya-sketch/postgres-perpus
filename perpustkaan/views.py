from django.shortcuts import render, get_object_or_404, redirect
from .models import Buku, Siswa, Peminjaman


# ─── BUKU VIEWS ────────────────────────────────────────────────

def dashboard(request):
    total_buku = Buku.objects.count()
    total_siswa = Siswa.objects.count()
    total_peminjaman = Peminjaman.objects.count()
    peminjaman_aktif = Peminjaman.objects.filter(status='Dipinjam').count()
    return render(request, 'perpustakaan/dashboard.html', {
        'total_buku': total_buku,
        'total_siswa': total_siswa,
        'total_peminjaman': total_peminjaman,
        'peminjaman_aktif': peminjaman_aktif,
    })

def buku_list(request):
    buku_list = Buku.objects.all()
    return render(request, 'buku/list.html', {'buku_list': buku_list})


def buku_tambah(request):
    if request.method == 'POST':
        Buku.objects.create(
            judul=request.POST['judul'],
            pengarang=request.POST['pengarang'],
            kategori=request.POST['kategori'],
            penerbit=request.POST['penerbit'],
            tahun_terbit=request.POST['tahun_terbit'],
            rak=request.POST['rak'],
            stok=request.POST['stok'],
            deskripsi=request.POST.get('deskripsi', ''),
        )
        return redirect('buku_list')
    return render(request, 'buku/tambah.html')


def buku_detail(request, pk):
    buku = get_object_or_404(Buku, pk=pk)
    return render(request, 'buku/detail.html', {'buku': buku})


def buku_edit(request, pk):
    buku = get_object_or_404(Buku, pk=pk)
    if request.method == 'POST':
        buku.judul = request.POST['judul']
        buku.pengarang = request.POST['pengarang']
        buku.kategori = request.POST['kategori']
        buku.penerbit = request.POST['penerbit']
        buku.tahun_terbit = request.POST['tahun_terbit']
        buku.rak = request.POST['rak']
        buku.stok = request.POST['stok']
        buku.deskripsi = request.POST.get('deskripsi', '')
        buku.save()
        return redirect('buku_list')
    return render(request, 'buku/edit.html', {'buku': buku})


def buku_delete(request, pk):
    buku = get_object_or_404(Buku, pk=pk)
    if request.method == 'POST':
        buku.delete()
        return redirect('buku_list')
    return render(request, 'buku/delete.html', {'buku': buku})


# ─── SISWA VIEWS ───────────────────────────────────────────────

def siswa_list(request):
    siswa_list = Siswa.objects.all()
    return render(request, 'siswa/list-siswa.html', {'siswa_list': siswa_list})


def siswa_tambah(request):
    if request.method == 'POST':
        # Bagian is_active sudah dihapus dari sini
        Siswa.objects.create(
            nama=request.POST['nama'],
            kelas=request.POST['kelas'],
            nis=request.POST['nis'],
        )
        return redirect('siswa_list')
    return render(request, 'siswa/tambah-siswa.html')


def siswa_detail(request, pk):
    siswa = get_object_or_404(Siswa, pk=pk)
    total_peminjaman = siswa.peminjaman.count()
    peminjaman_aktif_count = siswa.peminjaman.filter(status='Dipinjam').count()
    return render(request, 'siswa/detail-siswa.html', {
        'siswa': siswa,
        'total_peminjaman': total_peminjaman,
        'peminjaman_aktif_count': peminjaman_aktif_count,
    })


def siswa_edit(request, pk):
    siswa = get_object_or_404(Siswa, pk=pk)
    if request.method == 'POST':
        siswa.nama = request.POST['nama']
        siswa.kelas = request.POST['kelas']
        siswa.nis = request.POST['nis']
        # Bagian siswa.is_active sudah dihapus dari sini
        siswa.save()
        return redirect('siswa_list')
    return render(request, 'siswa/edit-siswa.html', {'siswa': siswa})


def siswa_hapus(request, pk):
    siswa = get_object_or_404(Siswa, pk=pk)
    if request.method == 'POST':
        siswa.delete()
        return redirect('siswa_list')
    return render(request, 'siswa/hapus-siswa.html', {'siswa': siswa})


# ─── PEMINJAMAN VIEWS ─────────────────────────────────────────

def peminjaman_list(request):
    peminjaman_list = Peminjaman.objects.select_related('siswa', 'buku').all()
    return render(request, 'peminjaman/list-peminjaman.html', {'peminjaman_list': peminjaman_list})


def peminjaman_tambah(request):
    if request.method == 'POST':
        siswa = get_object_or_404(Siswa, pk=request.POST['siswa_id'])
        buku = get_object_or_404(Buku, pk=request.POST['buku_id'])

        # Kurangi stok buku
        if buku.stok > 0:
            buku.stok -= 1
            buku.save()

        Peminjaman.objects.create(
            siswa=siswa,
            buku=buku,
            tanggal_pinjam=request.POST['tanggal_pinjam'],
            jatuh_tempo=request.POST['jatuh_tempo'],
            keperluan=request.POST.get('keperluan', ''),
            catatan=request.POST.get('catatan', ''),
            status='Dipinjam',
        )
        return redirect('peminjaman_list')

    # Bagian .filter(is_active=True) diganti menjadi .all()
    siswa_list = Siswa.objects.all()
    buku_list = Buku.objects.filter(stok__gt=0)
    return render(request, 'peminjaman/tambah-peminjaman.html', {
        'siswa_list': siswa_list,
        'buku_list': buku_list,
    })


def peminjaman_ubah_status(request, pk):
    peminjaman = get_object_or_404(Peminjaman, pk=pk)
    if request.method == 'POST':
        peminjaman.status = 'Dikembalikan'
        peminjaman.save()

        # Tambah stok buku kembali
        peminjaman.buku.stok += 1
        peminjaman.buku.save()

        return redirect('peminjaman_list')
    return render(request, 'peminjaman/ubah-status.html', {'peminjaman': peminjaman})