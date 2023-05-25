import psycopg2
from django.conf import settings

def create_connection():
    conn = psycopg2.connect(
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT'],
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD']
    )
    return conn

def get_rapat_data():
    try:
        conn = create_connection()
        cursor = conn.cursor()

        query = """
            SELECT 
                TP1.Nama_Tim || ' vs ' || TP2.Nama_Tim AS Rapat_Tim,
                NP.Nama_Depan || ' ' || NP.Nama_Belakang AS Nama_Panitia,
                S.Nama AS Stadium,
                R.Datetime AS Tanggal_Waktu,
                R.Isi_Rapat,
                R.ID_Pertandingan
            FROM 
                Rapat R
                JOIN Tim_Pertandingan TP1 ON TP1.ID_Pertandingan = R.ID_Pertandingan
                JOIN Tim_Pertandingan TP2 ON TP2.ID_Pertandingan = R.ID_Pertandingan
                JOIN Non_Pemain NP ON NP.ID = R.Perwakilan_Panitia
                JOIN Pertandingan P ON P.ID_Pertandingan = R.ID_Pertandingan
                JOIN Stadium S ON S.ID_Stadium = P.Stadium
            WHERE 
                TP1.Nama_Tim < TP2.Nama_Tim
        """

        cursor.execute(query)
        results = cursor.fetchall()

        return results

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching rapat data:", error)

    finally:
        if conn:
            cursor.close()
            conn.close()

def get_hasil_rapat(id_pertandingan):
    try:
        conn = create_connection()
        cursor = conn.cursor()

        query = """
            SELECT R.Hasil_Rapat
            FROM Rapat R
            WHERE R.ID_Pertandingan = %s
        """

        cursor.execute(query, (id_pertandingan,))
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return None

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching rapat hasil:", error)

    finally:
        if conn:
            cursor.close()
            conn.close()
