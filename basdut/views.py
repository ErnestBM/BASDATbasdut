from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from babadu_function.general import *
from babadu_function.authentication import *

# Create your views here.
def dashboard(request):
    if is_authenticated(request) == False:
        return HttpResponseRedirect(reverse('authentication:authentication'))

    # IF ROLE PANITIA LOGGED IN
    if request.COOKIES.get('user_role') == "PANITIA":
        # QUERY DATABASE
        user_id = request.COOKIES.get('user_id')
        nama_lengkap = parse(query_result(f"SELECT nama FROM member WHERE id='{user_id}';"))
        negara = parse(query_result(f"SELECT negara_asal FROM atlet WHERE id='{user_id}';"))
        email = parse(query_result(f"SELECT email FROM member WHERE id='{user_id}';"))
        tanggal_lahir = parse(query_result(f"SELECT tgl_lahir FROM atlet WHERE id='{user_id}';"))
        play = "Right" if parse(query_result(f"SELECT play_right FROM atlet WHERE id='{user_id}';")) else "Left"
        tinggi_badan = parse(query_result(f"SELECT height FROM atlet WHERE id='{user_id}';"))
        jenis_kelamin = "Laki" if parse(query_result(f"SELECT jenis_kelamin FROM atlet WHERE id='{user_id}';")) else "Perempuan"
        world_rank = "-" if parse(query_result(f"SELECT world_rank FROM atlet WHERE id='{user_id}';")) == None else "#"+str(parse(query_result(f"SELECT world_rank FROM atlet WHERE id='{user_id}';")))
        pelatih = parse(query_result(f"""
                                        SELECT nama
                                        FROM member
                                        JOIN atlet_pelatih ON member.id = atlet_pelatih.id_pelatih
                                        WHERE atlet_pelatih.id_atlet = '{user_id}';
                                        """
                                    ))
        print(query_result(f"SELECT * FROM atlet_non_kualifikasi WHERE id_atlet='{user_id}';"))
        status = "Qualified" if len(query_result(f"SELECT * FROM atlet_non_kualifikasi WHERE id_atlet='{user_id}';")) != 0 else "Not Qualified"
        total_poin = '0' if parse(query_result(f"SELECT SUM(total_point) FROM point_history WHERE id_atlet='{user_id}';")) == None else parse(query_result(f"SELECT SUM(total_point) FROM point_history WHERE id_atlet='{user_id}';"))
        # SET CONTEXT
        dummy_atlet = {
            "nama_lengkap": nama_lengkap,
            "negara": negara,
            "email": email,
            "tanggal_lahir": tanggal_lahir,
            "play": play,
            "tinggi_badan": f"{tinggi_badan}cm",
            "jenis_kelamin": jenis_kelamin,
            "pelatih": pelatih,
            "status": status,
            "world_rank": world_rank,
            "total_poin": total_poin,
        }
        return render(request, 'dashboard_atlet.html', dummy_atlet)
    
    # IF ROLE PELATIH LOGGED IN
    if request.COOKIES.get('user_role') == "PELATIH":
        user_id = request.COOKIES.get('user_id')
        nama_lengkap = parse(query_result(f"SELECT nama FROM member WHERE id='{user_id}';"))
        email = parse(query_result(f"SELECT email FROM member WHERE id='{user_id}';"))
        spesialisasi_id = parse(query_result(f"SELECT id_spesialisasi FROM pelatih_spesialisasi WHERE id_pelatih='{user_id}'"))
        spesialisasi_kategori = parse(query_result(f"SELECT spesialisasi FROM spesialisasi WHERE id='{spesialisasi_id}';"))
        tanggal_mulai = parse(query_result(f"SELECT tanggal_mulai FROM pelatih WHERE id='{user_id}';"))
        dummy_pelatih = {
            "nama_lengkap": nama_lengkap,
            "negara": "Indonesia",
            "email": email,
            "spesialisasi_kategori": spesialisasi_kategori,
            "tanggal_mulai": tanggal_mulai
        }
        return render(request, 'dashboard_pelatih.html', dummy_pelatih)

    # IF ROLE UMPIRE LOGGED IN
    if request.COOKIES.get('user_role') == "UMPIRE":
         # QUERY DATABASE
        user_id = request.COOKIES.get('user_id')
        nama_lengkap = parse(query_result(f"SELECT nama FROM member WHERE id='{user_id}';"))
        negara = parse(query_result(f"SELECT negara FROM umpire WHERE id='{user_id}';"))
        email = parse(query_result(f"SELECT email FROM member WHERE id='{user_id}';"))
        # SET CONTEXT
        dummy_umpire = {
            "nama_lengkap": nama_lengkap,
            "negara": negara,
            "email": email
        }
        return render(request, 'dashboard_umpire.html', dummy_umpire)