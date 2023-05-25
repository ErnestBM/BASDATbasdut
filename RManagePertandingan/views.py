from django.shortcuts import render, redirect
from django.db import connection
from utils.query import query
import json
from CRUDPembuatanPertandingan.views import fetch

# Create your views here.
def createNextPertandingan(request):
    return render(request, 'CreateNextPertandingan.html')

def managePertandingan(request):
    queryManage = """
    select  string_agg(tp.nama_tim, ' vs ') as tim_bertanding,
            to_char(p.start_datetime, 'Dy, YYYY Mon DD') as tanggal
            from pertandingan p
            join stadium s on p.stadium = s.id_stadium
            join tim_pertandingan tp on p.id_pertandingan = tp.id_pertandingan
            group by s.nama, p.id_pertandingan;
    """

    manage_pertandingan = query(queryManage)
    context = {'manage_pertandingan': manage_pertandingan}
    response = query(queryManage)
    print(manage_pertandingan)
    return render(request, 'managePertandingan.html', context)

def updatePertandingan(request):
    queryUpdate = """
    select  string_agg(tp.nama_tim, ' vs ') as tim_bertanding,
            to_char(p.start_datetime, 'Dy, YYYY Mon DD') as tanggal
            from pertandingan p
            join stadium s on p.stadium = s.id_stadium
            join tim_pertandingan tp on p.id_pertandingan = tp.id_pertandingan
            group by s.nama, p.id_pertandingan;
    """

    update_pertandingan = query(queryUpdate)
    context = {'update_pertandingan': update_pertandingan}
    response = query(queryUpdate)
    print(update_pertandingan)
    return render(request, 'updatePertandingan.html', context)

def endPertandingan(request):
    return render(request, 'EndPertandingan.html')

# def listPeristiwa(request):
#     return render(request, 'ListPeristiwa.html')

def panggilPeristiwa(request):

        queryPeristiwa = """
            select concat(P.nama_depan, ' ', P.nama_belakang) as nama, E.jenis
            from pemain p , peristiwa e 
            where e.id_pertandingan = 'b4c4c607-0432-4f54-966d-6709511dfa0a' and e.id_pemain=p.id_pemain
            and nama_tim = 'Dragons'
            """

        list_peristiwa = query(queryPeristiwa)
        context = {'list_peristiwa': list_peristiwa}
        response = query(queryPeristiwa)
        print(response)
        return render(request, 'ListPeristiwa.html', context)
        