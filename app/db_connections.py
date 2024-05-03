# myapp/db_connections.py

from django.conf import settings
from pymongo import MongoClient
import mysql.connector
import sqlite3

def get_mysql_connection():
    mysql_settings = settings.DATABASES['mysql']
    conn = mysql.connector.connect(
        host=mysql_settings['HOST'],
        port=mysql_settings['PORT'],
        user=mysql_settings['USER'],
        password=mysql_settings['PASSWORD'],
        database=mysql_settings['NAME']
    )
    return conn

def get_mongodb_connection():
    mongodb_settings = settings.MONGODB_DATABASES['default']
    conn = MongoClient(
        host=mongodb_settings['HOST'],
        port=mongodb_settings['PORT'],
        username=mongodb_settings['USER'],
        password=mongodb_settings['PASSWORD'],
        authSource=mongodb_settings['NAME']
    )
    db = conn[mongodb_settings['NAME']]
    return db

def get_sqlite_connection():
    conn = sqlite3.connect(settings.DATABASES['default']['NAME'])
    return conn
