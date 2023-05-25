from django.db import InternalError, IntegrityError
from django.shortcuts import redirect, render
from psycopg2.extras import RealDictCursor
from psycopg2.errors import UniqueViolation
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import psycopg2
# import query
# Create your views here.

def connect():
    connection = psycopg2.connect(user="postgres",
                        password="HbBv4Y89Ou3MOwHziV4Z",
                        host="containers-us-west-97.railway.app",
                        port="6458",
                        database="railway")
    return connection

def get_Manajer(request):
    
    connection = connect()
    cursor = connection.cursor()
    
    username = request.session.get('username')
    
    cursor.execute(f"SELECT id_manajer FROM MANAJER WHERE username = '{username}'") 
    result = cursor.fetchall()
    id_manajer = result[0][0]
     
    cursor.execute(f"SELECT nama_tim FROM TIM_MANAJER WHERE id_manajer = '{id_manajer}'")
    result = cursor.fetchall()
    if len(result) != 0:
        nama_tim = result[0][0]
    else:
        nama_tim = ""
        
    print(nama_tim)
    print(id_manajer)
    return (id_manajer, nama_tim)

def show_tim_form(request):
    connection = connect()
    cursor = connection.cursor()
    
    manajer_data = get_Manajer(request)
    id_manajer = manajer_data[0]
    nama_tim = manajer_data[1]
    
    if nama_tim=="":
        return render(request, "TimRegis/TimRegis.html")
    else:
        return redirect('CRUMengelolaTim:tim_detail')

@csrf_exempt
def show_dashboard_manajer(request):
    connection = connect()
    cursor = connection.cursor()
    
    manajer_data = get_Manajer(request)
    id_manajer = manajer_data[0]
    nama_tim = manajer_data[1]
    
    cursor.execute(f'''
                   SELECT *
                   FROM NON_PEMAIN
                   WHERE NON_PEMAIN.id='{id_manajer}'
                   ''')
    manajer_non_pemain = cursor.fetchall()
    
    cursor.execute(f'''
                   SELECT *
                   FROM STATUS_NON_PEMAIN
                   WHERE STATUS_NON_PEMAIN.id_non_pemain='{id_manajer}'
                   ''')
    status_non_pemain = cursor.fetchall()
        
    cursor.execute(f"""
                   SELECT *
                   FROM PEMAIN
                   WHERE PEMAIN.nama_tim='{nama_tim}';""")
    pemain_data = cursor.fetchall()
    x = []
    for row in pemain_data:
        x.append('%s %s' % (row[2], row[3]))
        
    cursor.execute(f"""
                   SELECT *
                   FROM PELATIH
                   WHERE PELATIH.Nama_Tim='{nama_tim}';""")
    pelatih_data = cursor.fetchall()
    y = []
    for row in pelatih_data:
        y.append(row[0])
    
    if len(pelatih_data) == 1:
        cursor.execute(f'''SELECT *
                       FROM NON_PEMAIN
                       WHERE NON_PEMAIN.id='{y[0]}';
                       ''')
        pelatih_non_pemain = cursor.fetchall()
        y.clear()
        for row in pelatih_non_pemain:
            y.append('%s %s' % (row[1], row[2]))
    
    elif len(pelatih_data) == 2:
        cursor.execute(f'''SELECT *
                       FROM NON_PEMAIN
                       WHERE NON_PEMAIN.id='{y[0]}' OR NON_PEMAIN.id='{y[1]}';
                       ''')
        pelatih_non_pemain = cursor.fetchall()
        y.clear()
        for row in pelatih_non_pemain:
            y.append('%s %s' % (row[1], row[2]))
    
    elif len(pelatih_data) == 0:
        y.clear()
        
    
    context = {
        "nama_tim" : nama_tim,
        "pemain_data" : x,
        "pelatih_data" : y,
        "id" : manajer_non_pemain[0][0],
        "nama": ('%s %s' % (manajer_non_pemain[0][1], manajer_non_pemain[0][2])),
        "no_hp": manajer_non_pemain[0][3],
        "email": manajer_non_pemain[0][4],
        "alamat": manajer_non_pemain[0][5],
        "status": status_non_pemain[0][1]
    }
    
    return render(request, 'DashboardManager/DashBoard.html', context)

def register_tim(request):
    connection = connect()
    cursor = connection.cursor()
    
    manajer_data = get_Manajer(request)
    id_manajer = manajer_data[0]

    nama_tim_registrasi = request.POST.get('nama_tim')
    nama_universitas_registrasi = request.POST.get('universitas')
    
    cursor.execute(f"""INSERT INTO TIM VALUES ('{nama_tim_registrasi}', '{nama_universitas_registrasi}')""")
    cursor.execute(f"""INSERT INTO TIM_MANAJER (id_manajer, nama_tim) VALUES ('{id_manajer}', '{nama_tim_registrasi}')""")

    
    connection.commit()
    connection.close()
    print("Database is Closed and Values has been Added")
    
    return redirect('CRUMengelolaTim:dashboard_manajer')        

def get_pemain_pelatih(request):
    connection = connect()
    cursor = connection.cursor()
        
    manajer_data = get_Manajer(request)
    id_manajer = manajer_data[0]
    nama_tim = manajer_data[1]
        
    cursor.execute(f"""
                   SELECT nama_depan, nama_belakang, nomor_hp, tgl_lahir, is_captain, posisi, npm, jenjang
                   FROM PEMAIN
                   WHERE PEMAIN.nama_tim='{nama_tim}';""")
    pemain_data = cursor.fetchall()
    
    x = []
    for row in pemain_data:
        x.append(row)
        
    cursor.execute(f"""
                   SELECT *
                   FROM PELATIH
                   WHERE PELATIH.Nama_Tim='{nama_tim}';""")
    pelatih_data = cursor.fetchall()
    y = []
    for row in pelatih_data:
        y.append(row[0])
    
    if len(y) == 2:
        cursor.execute(f"""
                    SELECT nama_depan, nama_belakang, nomor_hp, email, alamat, spesialisasi
                    FROM NON_PEMAIN, SPESIALISASI_PELATIH
                    WHERE NON_PEMAIN.id='{y[0]}' AND SPESIALISASI_PELATIH.id_pelatih='{y[0]}';""")
        pelatih_non_pemain_data1 = cursor.fetchall()
        
        cursor.execute(f"""
                    SELECT nama_depan, nama_belakang, nomor_hp, email, alamat, spesialisasi
                    FROM NON_PEMAIN, SPESIALISASI_PELATIH
                    WHERE NON_PEMAIN.id='{y[1]}' AND SPESIALISASI_PELATIH.id_pelatih='{y[1]}';""")
        pelatih_non_pemain_data2 = cursor.fetchall()
        y.clear()
        
        y.append(pelatih_non_pemain_data1[0])
        y.append(pelatih_non_pemain_data2[0])        
    
    elif len(y) == 1:
        cursor.execute(f"""
                    SELECT nama_depan, nama_belakang, nomor_hp, email, alamat, spesialisasi
                    FROM NON_PEMAIN, SPESIALISASI_PELATIH
                    WHERE NON_PEMAIN.id='{y[0]}' AND SPESIALISASI_PELATIH.id_pelatih='{y[0]}';""")
        pelatih_non_pemain_data = cursor.fetchall()
    
        y.clear()
        for row in pelatih_non_pemain_data:    
            y.append(row)
    
    context = {
        "nama_tim" : nama_tim,
        "pemain_data" : x,
        "pelatih_data" : y,
    }

    return render(request, 'TimPage/TimDetail.html', context)

def pemilihan_pemain(request):
    
    connection = connect()
    cursor = connection.cursor()
    
    cursor.execute(f"""
                   SELECT nama_depan, nama_belakang, posisi
                   FROM PEMAIN
                   WHERE PEMAIN.nama_tim='null';""")
    pemain_data = cursor.fetchall()
    
    x = []
    for row in pemain_data:
        x.append(row)
        
    context = {
        "pemain_data" : pemain_data,
    }
    
    return render(request, "PemilihanPemain/PemilihanPemain.html", context)

def pemilihan_pelatih(request):
    
    connection = connect()
    cursor = connection.cursor()
    
    cursor.execute(f"""
                   SELECT id_pelatih
                   FROM PELATIH
                   WHERE PELATIH.nama_tim=null;""")
    pelatih_data = cursor.fetchall()
    
    x = []
    for row in pelatih_data:
        x.append(row)
    
    if len(x) !=0:
        cursor.execute(f"""
                    SELECT nama_depan, nama_belakang
                    FROM NON_PEMAIN
                    WHERE NON_PEMAIN.id='{x[0]}';""")
        pelatih_data = cursor.fetchall()
        
        x = []
        for row in pelatih_data:
            x.append(row)
            
        context = {
            "pelatih_data" : pelatih_data,
        }
    
    else:
        context = {
            "pelatih_data" : pelatih_data,
        }
    
    return render(request, "PemilihanPemain/PemilihanPelatih.html", context)
    
    
    
    
    