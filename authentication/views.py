from django.shortcuts import render, redirect
from django.db import connection, InternalError
from django.shortcuts import redirect, render
from django.db import IntegrityError, connections
import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.errors import UniqueViolation
from django.http import HttpResponse, HttpRequest
import uuid
from utils.query import query


# Create your views here.

connection = psycopg2.connect(user="postgres",
                        password="HbBv4Y89Ou3MOwHziV4Z",
                        host="containers-us-west-97.railway.app",
                        port="6458",
                        database="railway")


def login(request):
    if (request.session.get('username') != None):
        return redirect(f'''/{request.session.get('role')}/''')
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        response = query(f''' SELECT * FROM USER_SYSTEM WHERE username = '{username}' 
        AND password = '{password}' ''')
        if len(response) == 0:
            context['messages'] = 'Username atau Password Salah'
            return render(request, 'login/login.html', context)
        else:
            request.session['username'] = username
            find_user = f''' SELECT * FROM MANAJER WHERE username = '{username}' '''
            response = query(find_user)
            if len(response) == 0:
                find_user = f''' SELECT * FROM PANITIA WHERE username = '{username}' '''
                response = query(find_user)
                if len(response) == 0:
                    request.session["role"] = "penonton"
                    return redirect('/show_dashboard_penonton/')  
                
                else:
                    request.session["role"] = "panitia" 
                    return redirect('/show_dashboard_panitia/')
            else:
                request.session["role"] = "manajer"
                return redirect('/show_dashboard_manajer/')
                   
    
    return render(request, 'login/login.html', context)


def show_authentication(request):
    if (request.session.get('username') != None):
        return redirect(f'''/{request.session.get('role')}/''')    
    context = {}
    return render(request, "mainpage/mainpage.html", context)

def show_register(request):
    if (request.session.get('username') != None):
        return redirect(f'''/{request.session.get('role')}/''')
    return render(request, "registerwho/jenisregister.html")
def show_register_panitia(request):
    if (request.session.get('username') != None):
        return redirect(f'''/{request.session.get('role')}/''')
    return render(request, "register/registerpanitia.html")
def show_register_lain(request):
    if (request.session.get('username') != None):
        return redirect(f'''/{request.session.get('role')}/''')
    return render(request, "register/register.html")
    


def register_panitia(request):
    if (request.session.get('username') != None):
        return redirect(f'''/{request.session.get('role')}/''')
    id = uuid.uuid4()
    username = request.POST.get("username")
    password = request.POST.get("password")
    nama_depan = request.POST.get("nama_depan")
    nama_belakang = request.POST.get("nama_belakang")
    email = request.POST.get("email")
    no_hp = request.POST.get("phoneNumber")
    alamat = request.POST.get("address")
    non_pemain_status = request.POST.getlist("status")
    jabatan = request.POST.get("jabatan")
    insert_user = f''' INSERT INTO USER_SYSTEM VALUES ('{username}', '{password}')
    '''
    insert_non_pemain = f''' INSERT INTO NON_PEMAIN (id, nama_depan, nama_belakang, 
        nomor_hp, email, alamat) VALUES ('{id}', '{nama_depan}', '{nama_belakang}', 
        {no_hp},'{email}', '{alamat}')'''
    response = query(insert_user)
    if isinstance(response, Exception):
        # return to register_manajer.html, with error message
        print(response)
        context = {
            'messages': 'Username Sudah Terdaftar',
        }
        return render(request, 'register/registerpanitia.html', context)
    response = query(insert_non_pemain)
    for status in non_pemain_status:
        response = query(f''' INSERT INTO STATUS_NON_PEMAIN VALUES ('{id}', '{status}')''')
    response = query(f''' INSERT INTO PANITIA VALUES ('{id}' , '{jabatan}', '{username}')''')

    return redirect("authentication:login") 

def register_lain(request):
    if (request.session.get('username') != None):
        return redirect(f'''/{request.session.get('role')}/''')
    id = uuid.uuid4()
    username = request.POST.get("username")
    password = request.POST.get("password")
    nama_depan = request.POST.get("nama_depan")
    nama_belakang = request.POST.get("nama_belakang")
    email = request.POST.get("email")
    no_hp = request.POST.get("phoneNumber")
    alamat = request.POST.get("address")
    non_pemain_status = request.POST.getlist("status")
    role = request.POST.get("role")
    print(role)
    insert_user = f''' INSERT INTO USER_SYSTEM VALUES ('{username}', '{password}')
    '''
    insert_non_pemain = f''' INSERT INTO NON_PEMAIN (id, nama_depan, nama_belakang, 
        nomor_hp, email, alamat) VALUES ('{id}', '{nama_depan}', '{nama_belakang}', 
        {no_hp},'{email}', '{alamat}')'''
    response = query(insert_user)
    if isinstance(response, Exception):
        # return to register_manajer.html, with error message
        print(response)
        context = {
            'messages': 'Username Sudah Terdaftar',
        }
        return render(request, 'register/register.html', context)
    response = query(insert_non_pemain)
    for status in non_pemain_status:
        response = query(f''' INSERT INTO 
        STATUS_NON_PEMAIN VALUES ('{id}', '{status}')''')
    if (role == 'manajer'):
        response = query(f''' INSERT INTO MANAJER VALUES ('{id}' , '{username}')''')
    elif (role == 'penonton'):
        response = query(f''' INSERT INTO PENONTON VALUES ('{id}' , '{username}')''')
    return redirect("authentication:login") 


def get_uuid(request):
    query = f"SELECT id_panitia FROM panitia WHERE username = '{request.session['username']}';"
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchone()[0]

def show_dashboard_panitia(request):
    uuid_panitia = get_uuid(request)

    query_non_pemain = f"SELECT * FROM non_pemain WHERE id = '{uuid_panitia}';"
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query_non_pemain)
    query_np_result = cursor.fetchone()

    fname = query_np_result[1]
    lname = query_np_result[2]
    no_hp = query_np_result[3]
    email = query_np_result[4]
    alamat = query_np_result[5]

    query_panitia = f"SELECT * FROM panitia WHERE id_panitia = '{uuid_panitia}';"
    cursor.execute(query_panitia)
    query_p_result = cursor.fetchone()

    jabatan = query_p_result[1]
    username = query_p_result[2]

    query_status = f"SELECT * FROM status_non_pemain WHERE id_non_pemain = '{uuid_panitia}';"
    cursor.execute(query_status)
    query_s_result = cursor.fetchone()
    status = query_s_result[1]

    query_rapat = f"SELECT * FROM rapat WHERE perwakilan_panitia = '{uuid_panitia}';"
    cursor.execute(query_rapat)
    query_r_result = cursor.fetchall()
    query_r_result_list = []
    
    for row in query_r_result:
        # Query the manager's name based on the manager ID for team A
        manajer_id = row["manajer_tim_a"]
        manajer_query = f"SELECT username FROM manajer WHERE id_manajer = '{manajer_id}';"
        cursor.execute(manajer_query)
        manajer_result = cursor.fetchone()
        if manajer_result:
            row["manajer_tim_a"] = manajer_result[0]

        # Query the manager's name based on the manager ID for team B
        manajer_id = row["manajer_tim_b"]
        manajer_query = f"SELECT username FROM manajer WHERE id_manajer = '{manajer_id}';"
        cursor.execute(manajer_query)
        manajer_result = cursor.fetchone()
        if manajer_result:
            row["manajer_tim_b"] = manajer_result[0]

        query_r_result_list.append(dict(row))

    context = {
        "username": username,
        "uuid": uuid_panitia,
        "fname": fname,
        "lname": lname,
        "no_hp": no_hp,
        "email": email,
        "alamat": alamat,
        "jabatan": jabatan,
        "status": status,
        "rapat": query_r_result_list,
    }
    return render(request, "dashboard_panitia.html", context)


# def show_dashboard_penonton(request):
#     return render(request, "dashboard_penonton.html")

# def show_dashboard_manajer(request):
#     return render(request, "dashboard_manajer.html")

def show_dashboard_manajer(request):
    uuid_manajer = get_uuid(request)

    query_non_pemain = f"SELECT * FROM non_pemain WHERE id = '{uuid_manajer}';"
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query_non_pemain)
    query_np_result = cursor.fetchone()

    fname = query_np_result[1]
    lname = query_np_result[2]
    no_hp = query_np_result[3]
    email = query_np_result[4]
    alamat = query_np_result[5]

    query_status = f"SELECT * FROM status_non_pemain WHERE id_non_pemain = '{uuid_manajer}';"
    cursor.execute(query_status)
    query_s_result = cursor.fetchone()
    status = query_s_result[1]

    query_tim = f"""
    SELECT *
    FROM TIM AS t
    JOIN TIM_MANAJER tm ON t.nama_tim = tm.nama_tim AND tm.id_manajer = '{uuid_manajer}';
    """
    cursor.execute(query_tim)
    query_tim_result = cursor.fetchone()

    nama_tim = ""
    tim_universitas = ""
    if query_tim_result:
        nama_tim = query_tim_result[0]
        tim_universitas = query_tim_result[1]

    context = {
        "uuid": uuid_manajer,
        "fname": fname,
        "lname": lname,
        "no_hp": no_hp,
        "email": email,
        "alamat": alamat,
        "status": status,
        "nama_tim": nama_tim,
        "tim_universitas": tim_universitas
    }
    return render(request, "dashboard_manajer.html", context)


def show_dashboard_penonton(request):
    uuid_penonton = get_uuid(request)

    query_non_pemain = f"SELECT * FROM non_pemain WHERE id = '{uuid_penonton}';"
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query_non_pemain)
    query_np_result = cursor.fetchone()

    fname = query_np_result[1]
    lname = query_np_result[2]
    no_hp = query_np_result[3]
    email = query_np_result[4]
    alamat = query_np_result[5]

    query_status = f"SELECT * FROM status_non_pemain WHERE id_non_pemain = '{uuid_penonton}';"
    cursor.execute(query_status)
    query_s_result = cursor.fetchone()
    status = query_s_result[1]

    query_pertandingan = f"""
    SELECT p.id_pertandingan, p.start_datetime, p.end_datetime, s.nama
    FROM PERTANDINGAN AS p
    JOIN PEMBELIAN_TIKET pt ON p.id_pertandingan = pt.id_pertandingan
    JOIN STADIUM s ON p.stadium = s.id_stadium
    WHERE pt.id_penonton = '{uuid_penonton}' AND p.end_datetime > NOW();
    """
    cursor.execute(query_pertandingan)
    query_pertandingan_result = cursor.fetchall()
    query_pertandingan_result_list = []
    for row in query_pertandingan_result:
        query_pertandingan_result_list.append(dict(row))

    context = {
        "fname": fname,
        "lname": lname,
        "no_hp": no_hp,
        "email": email,
        "alamat": alamat,
        "status": status,
        "pertandingan": query_pertandingan_result_list,
    }
    return render(request, "dashboard_penonton.html", context)



def logout(request):
    request.session.flush()
    return redirect('/')