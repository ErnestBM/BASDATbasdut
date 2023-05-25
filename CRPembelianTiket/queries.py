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

def insert_pembelian_tiket(id_penonton, jenis_tiket, jenis_pembayaran, id_pertandingan):
    conn = create_connection()

    try:
        cursor = conn.cursor()

        query = """
            INSERT INTO pembelian_tiket (id_penonton, jenis_tiket, jenis_pembayaran, id_pertandingan)
            VALUES (%s, %s, %s, %s)
            RETURNING nomor_receipt
        """
        values = (id_penonton, jenis_tiket, jenis_pembayaran, id_pertandingan)

        cursor.execute(query, values)
        nomor_receipt = cursor.fetchone()[0]
        conn.commit()

        print("Pembelian tiket inserted successfully!")
        print("Nomor Receipt:", nomor_receipt)

    except (Exception, psycopg2.Error) as error:
        print("Error while inserting pembelian tiket:", error)

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")


def get_tim_pairs(stadium, tanggal):
    conn = create_connection()
    query = """
        SELECT TP1.Nama_Tim AS Tim_1, TP2.Nama_Tim AS Tim_2
        FROM Tim_Pertandingan TP1
        JOIN Tim_Pertandingan TP2 ON TP1.ID_Pertandingan = TP2.ID_Pertandingan
        JOIN Pertandingan P ON P.ID_Pertandingan = TP1.ID_Pertandingan
        JOIN Stadium S ON P.Stadium = S.ID_Stadium
        WHERE (TP1.Nama_Tim < TP2.Nama_Tim) AND (P.Start_Datetime = %s OR P.Start_Datetime = %s) AND S.Nama = %s
    """
    try:
        cur = conn.cursor()
        cur.execute(query, (tanggal, tanggal, stadium))
        results = cur.fetchall()
        return results

    except (Exception, psycopg2.Error) as error:
        print("Error while executing the query:", error)

    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")
