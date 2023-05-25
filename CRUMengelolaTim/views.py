from django.db import InternalError, IntegrityError
from django.shortcuts import redirect, render
from psycopg2.extras import RealDictCursor
from psycopg2.errors import UniqueViolation
from django.http import HttpResponse, HttpRequest, JsonResponse
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
    return (id_manajer, nama_tim)

def show_tim_form(request):
    return render(request, "TimRegis/TimRegis.html")

def show_dashboard_manajer(request):
    return render(request, 'DashboardManager/DarhBoard.html')
        

def register_tim(request):
    connection = connect()
    cursor = connection.cursor()
    
    manajer_data = get_Manajer(request)
    
    id_manajer = manajer_data[0]
    print(id_manajer)
    nama_tim = manajer_data[1]
    print(nama_tim)
        
    if not nama_tim:
        if (request.method == "POST"):        
            nama_tim_registrasi = request.POST.get('nama_tim')
            nama_universitas_registrasi = request.POST.get('nama_tim')
            
            cursor.execute(f"""
                           INSERT INTO TIM VALUES
                           ('{nama_tim_registrasi}', '{nama_universitas_registrasi}');
                           """)
            cursor.execute(f"""INSERT INTO TIM_MANAJER VALUES ('{id_manajer}', '{nama_tim_registrasi}');""")
            
            if connection:
                connection.commit()
                connection.close()
                print("Database is Closed and Values has been Added")
                
        return render(request, 'TimRegis/TimRegis.html')
    else:
        return redirect('CRUMengelolaTim:tim_detail')
        

def get_pemain_pelatih(request):
    connection = connect()
    cursor = connection.cursor()
        
    manajer_data = get_Manajer(request)
    id_manajer = manajer_data[0]
    nama_tim = manajer_data[1]
    cursor.execute(f"""
                   SELECT *
                   FROM TIM
                   WHERE TIM.nama_tim={nama_tim};""")
    tim_data = cursor.fetchall()
    for row in tim_data:
        print("Nama Tim: ", row[0])
        print("Universitas: ", row[1])
        
    cursor.execute(f"""
                   SELECT *
                   FROM PEMAIN
                   WHERE PEMAIN.nama_tim={nama_tim};""")
    pemain_data = cursor.fetchall()
    for row in pemain_data:
        print("ID Pemain: ", row[0])
        print("Nama Tim: ", row[1])
        
    cursor.execute(f"""
                   SELECT *
                   FROM PELATIH
                   WHERE PELATIH.Nama_Tim={nama_tim};""")
    pelatih_data = cursor.fetchall()
    for row in pelatih_data:
        print("ID Pelatih: ", row[0])
        print("Nama Tim: ", row[1])

    return render(request, 'TimPage/TimDetail.html')
        