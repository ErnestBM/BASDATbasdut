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

# def delete_pertandingan(request, pertandingan_id):
#     pertandingan = get_object_or_404(Pertandingan, id=pertandingan_id)
#     pertandingan.delete()
#     return JsonResponse({'message': 'Pertandingan deleted successfully'})

def fetch(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# def addStadium(request):
#     query = """
#             SELECT S.Nama
#             FROM Stadium AS S;
#             """
#     cursor = connection.cursor()
#             cursor.execute('SET search_path TO babadu;')
#             cursor.execute(query)
#             data = fetch(cursor)

#                 response = {'data': data}
#                 print(response)
#                 return render(request, 'TanggalPembuatan.html', response)
            
#             elif request.method == 'POST' :
#                 id_pelatih = '841be0cc-9587-4164-b6eb-75cac8e62f17' # request.session['id_pelatih']
#                 id_atlet = request.POST['id_atlet']

#                 query = f"""
#                     INSERT INTO ATLET_PELATIH VALUES ('{id_pelatih}', '{id_atlet}');
#                 """
#                 cursor = connection.cursor()
#                 cursor.execute('SET search_path TO babadu;')
#                 cursor.execute(query)

#                 return redirect('pink:r_latih_atlet')
