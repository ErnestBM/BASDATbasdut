from django.shortcuts import render
from django.db import connection, InternalError

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

    context = {}
    return render(request, 'login.html', context)

def convert(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def show_login(request):
    print('ee')
    cursor = connection.cursor()
    cursor.execute("set search_path to SEPAKBOLA;")
    cursor.execute('SELECT * FROM TIM;')
    res = convert(cursor)
    print('rhdehd')
    print(res)
    context = {}
    return render(request, "login.html", context)