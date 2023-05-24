from django.shortcuts import render, redirect
from django.db import connection, InternalError
from psycopg2 import cursor



# Create your views here.

def login(request):
    print('eee')
    
    if request.method == 'POST':
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        # query = get_user_query(nama, email)
        # request.session['is_atlet'] = False
        # request.session['is_pelatih'] = False
        # request.session['is_umpire'] = False
        # if len(res) == 1:
        #     mem = res[0]
        #     for attr in mem:
        #         if isinstance(mem[attr], uuid.UUID):
        #             request.session[attr] = str(mem[attr])
        #         elif isinstance(mem[attr], datetime.date):
        #             date = datetime.datetime.strptime(str(mem[attr]), '%Y-%m-%d')
        #             formatted_date = date.strftime('%d %B %Y')
        #             request.session[attr] = formatted_date
        #         else:
        #             request.session[attr] = mem[attr]
        #     request.session[SESSION_ROLE_KEYS[mem['member_type']]] = True
        #     return redirect('/dashboard')     
        # else:
        #     messages.info(request,'Username atau Password salah')
    conn = psycopg2.connect(DATABASES)
    cursor.execute("SELECT * FROM TIM")
    Tim = cursor.fetchall()
    context = {'tim': Tim, 'test': "test mek"}
    return render(request, 'authentication.html', context)

def convert(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# def show_login(request):
#     # print('ee')
#     # cursor = connection.cursor()

#     # res = convert(cursor)
#     # print('rhdehd')
#     # print(res)
#     context = {}
#     return render(request, "login.html", context)

def show_authentication(request):
    context = {}
    return render(request, "authentication.html", context)

def show_register(request):
    return render(request, "register.html")
def show_register_panitia(request):
    return render(request, "register_panitia.html")
def show_register_lain(request):
    return render(request, "register_lain.html")
    
def logout(request):
    request.session.flush()
    return redirect('/')