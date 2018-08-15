import os

SECRET_KEY = os.urandom(24)
DEBUG = True

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'supervisor'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = 'mysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True