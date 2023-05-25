from django.db import connection
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


# Create your views here.

def buatPertandingan(request):
    context = {}
    return render(request, "BuatPertandingan.html", context)

def listStadium(request):
    context = {}
    return render(request, "ListStadium.html", context)

def listWaktu(request):
    context = {}
    return render(request, "TanggalPembuatan.html", context)

def listWasit(request):
    context = {}
    return render(request, "PemilihanWasit.html", context)


def fetch(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


