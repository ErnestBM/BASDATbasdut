from django.shortcuts import redirect, render
from queries import *
from authentication.views import *
# Create your views here.

def show_tipe_stadium(request):
    if request.method == 'POST':
        selected_stadium = request.POST.get('selector')
        selected_date = request.POST.get('Tanggal')

        return redirect('show_waktu_stadium', stadium=selected_stadium, date=selected_date)
    
    return render(request, 'TipeStadium.html')

def show_waktu_stadium(request, selected_stadium, selected_date):
    request.session['selected_stadium'] = selected_stadium
    request.session['selected_date'] = selected_date
    
    return redirect('list_pertandingan', stadium=selected_stadium, date=selected_date)


def show_list_pertandingan(request, selected_stadium, selected_date):
    tim_pairs = get_tim_pairs(selected_stadium, selected_date)
    data = []
    for pair in tim_pairs:
        tim_1 = pair[0]
        tim_2 = pair[1]
        action = f'<a href="/show_beli_tiket/{tim_1}/{tim_2}">Pilih</a>'
        data.append([tim_1, tim_2, action])

    return render(request, 'list_pertandingan.html', {'data': data})

def show_beli_tiket(request, id_pertandingan):
    if request.method == 'POST':
        jenis_tiket = request.POST.get('jenis_tiket')
        jenis_pembayaran = request.POST.get('jenis_pembayaran')
        id_penonton = get_logged_in_user_id()

        insert_pembelian_tiket(id_penonton, jenis_tiket, jenis_pembayaran, id_pertandingan)
        
        return redirect('dashboard')
    
    return render(request, 'BeliTiket.html')


