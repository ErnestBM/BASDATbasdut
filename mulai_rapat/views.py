from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from utils.query import *
import datetime

def show_mulai_rapat(request,uuid,teams):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'panitia':

            context = {
                'teams': teams,
                'role':'panitia',
            }

            if request.method == "POST":
                teams = teams.split(" vs ")
                team1 = teams[0]
                team2 = teams[1]

                cursor.execute(f'''
                                SELECT id_manajer 
                                FROM tim_manajer 
                                WHERE nama_tim = \'{team1}\' 
                                ''')
                team1manager = cursor.fetchmany()[0][0]

                cursor.execute(f''' SELECT id_manajer 
                                    FROM tim_manajer 
                                    WHERE nama_tim = \'{team2}\' 
                                    ''')
                team2manager = cursor.fetchmany()[0][0]

                cursor.execute(f''' SELECT (start_datetime - interval '10 days') 
                                    FROM pertandingan 
                                    WHERE id_pertandingan = \'{uuid}\'
                                    ''')
                getdate = cursor.fetchmany()[0][0]

                cursor.execute(f''' SELECT p.id_panitia 
                                    FROM panitia p 
                                    WHERE p.id_panitia NOT IN (
                                        SELECT rapat.perwakilan_panitia 
                                        FROM rapat 
                                        WHERE (manajer_tim_a = \'{team1manager}\' AND manajer_tim_b = \'{team2manager}\') 
                                        OR (manajer_tim_a = \'{team2manager}\' AND manajer_tim_b = \'{team1manager}\') );
                                        ''')
                idpanitia = cursor.fetchmany()[0][0]
                
                text = request.POST.get('isi')

                cursor.execute(f'''
                                    INSERT INTO Rapat (ID_Pertandingan, Datetime, Perwakilan_Panitia, Manajer_Tim_A, Manajer_Tim_B, Isi_Rapat) VALUES 
                                    (\'{uuid}\', \'{getdate}\', \'{idpanitia}\', \'{team1manager}\', \'{team2manager}\', \'{text}\');
                                    ''')
                connection.commit()

                return HttpResponseRedirect(reverse('example_app:dashboard'))

            return render(request, 'mulaiRapat.html', context)
        else:
            return HttpResponseRedirect(reverse('example_app:index'))
    else:
        return HttpResponseRedirect(reverse('example_app:index'))

def show_isi_rapat(request):
    if request.COOKIES.get('role'):
        if request.COOKIES.get('role') == 'panitia':
            command = '''
            SELECT STRING_AGG(TP.nama_tim, ' vs ') AS tim_tanding,
                S.nama,
                P.start_datetime,
                P.end_datetime,
                P.id_pertandingan
            FROM Pertandingan P
            JOIN Tim_Pertandingan TP ON TP.id_pertandingan = P.id_pertandingan
            JOIN stadium S ON S.id_stadium = P.stadium
            LEFT JOIN rapat R ON R.id_pertandingan = P.id_pertandingan
            WHERE R.id_pertandingan IS NULL
            GROUP BY P.id_pertandingan, S.nama;
            '''

            cursor.execute(command)

            isi_rapat = cursor.fetchall()



            context = {
                'isi_rapat': isi_rapat,
                'role':'panitia',
            }
            return render(request, "isi_rapat.html", context)
        else:
            return HttpResponseRedirect(reverse('index.html'))
    else:
        return HttpResponseRedirect(reverse('index.html'))
