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