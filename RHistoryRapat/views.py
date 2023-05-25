from django.shortcuts import render

from .queries import *

def show_list_rapat(request):
    rapat_data = get_rapat_data()
    data = []
    for rapat in rapat_data:
        tim_1 = rapat[0]
        tim_2 = rapat[1]
        nama_panitia = rapat[2]
        stadium = rapat[3]
        datetime = rapat[4]
        id_pertandingan = rapat[5]
        action = f'<a href="/lihat_hasil_rapat/{id_pertandingan}">Lihat Hasil Rapat</a>'
        data.append([f'{tim_1} vs {tim_2}', nama_panitia, stadium, datetime, action])

    return render(request, 'HistoryRapat.html', {'data': data})

def show_hasil_rapat(request, id_pertandingan):
    hasil_rapat = get_hasil_rapat(id_pertandingan)

    return render(request, 'hasil_rapat.html', {'hasil_rapat': hasil_rapat})