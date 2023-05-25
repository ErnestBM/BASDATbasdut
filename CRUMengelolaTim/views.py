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


def get_manajer_non_pemain(request):
    connection = connect()
    cursor = connection.cursor()
    
    manajer_data = get_Manajer(request)
    id_manajer = manajer_data[0]
    nama_tim = manajer_data[1]
        
    context = {
        "id" : manajer_non_pemain[0],
        "nama": '%s %s' % (manajer_non_pemain[1], manajer_non_pemain[2]),
        "no_hp": manajer_non_pemain[3],
        "email": manajer_non_pemain[4],
        "alamat": manajer_non_pemain[5],
        "status": status_non_pemain[0]
    }
    
    return (context)

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
                   SELECT *
                   FROM TIM
                   WHERE TIM.nama_tim='{nama_tim}';""")
    tim_data = cursor.fetchall()
    for row in tim_data:
        print("Nama Tim: ", row[0])
        print("Universitas: ", row[1])
        
    cursor.execute(f"""
                   SELECT *
                   FROM PEMAIN
                   WHERE PEMAIN.nama_tim='{nama_tim}';""")
    pemain_data = cursor.fetchall()
    
    x = []
    for row in pemain_data:
        print("ID Pemain: ", row[0])
        print("Nama Tim: ", row[1])
        x.append(row)
        
        
    cursor.execute(f"""
                   SELECT *
                   FROM PELATIH
                   WHERE PELATIH.Nama_Tim='{nama_tim}';""")
    pelatih_data = cursor.fetchall()
    y = []
    for row in pelatih_data:
        print("ID Pelatih: ", row[0])
        print("Nama Tim: ", row[1])
        y.append(row)
    
    context = {
        "nama_tim" : nama_tim,
        "pemain_data" : x,
        "pelatih_data" : y,
    }

    return render(request, 'TimPage/TimDetail.html', context)
        