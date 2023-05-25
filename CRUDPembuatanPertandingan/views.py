from django.shortcuts import render

# Create your views here.

def show_buat_pertandingan(request):
    context = {}
    return render(request, "BuatPertandingan.html", context)

def show_list_stadium(request):
    context = {}
    return render(request, "ListStadium.html", context)

def show_list_waktu(request):
    context = {}
    return render(request, "TanggalPembuatan.html", context)

def show_list_wasit(request):
    context = {}
    return render(request, "PemilihanWasit.html", context)