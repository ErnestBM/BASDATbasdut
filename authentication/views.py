from django.shortcuts import render, redirect
from django.db import connection, InternalError
from django.shortcuts import redirect, render
from django.db import IntegrityError, connections
from psycopg2.extras import RealDictCursor
from psycopg2.errors import UniqueViolation
from django.http import HttpResponse, HttpRequest
import uuid
# import query
from utils.query import query


# Create your views here.

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
                    return redirect('/penonton')  
                
                else:
                    request.session["role"] = "panitia" 
                    return redirect('/panitia')
            else:
                request.session["role"] = "manajer"
                return redirect('/manajer')
                   
    
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

    

def logout(request):
    request.session.flush()
    return redirect('/')