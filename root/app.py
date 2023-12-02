# ------- Biblioteki -------
# Zewnetrzne biblioteki
import sqlite3
import os
from flask import Flask, flash, render_template
from flask import g 
from dotenv import load_dotenv

# Wewnetrzne biblioteki
from modules.db_utils import *
from modules.credentials_helper import UserPass
from pages.menu import Menu


# ------- Inicjalizacja Modulow -------
app = Flask(__name__, template_folder='components')   # Instancja aplikacji Flask


# ------- Konfiguracja -------
load_dotenv()   # Wczytanie zmiennych srodowiskowych z .env
app.config['SECRET_KEY'] =  os.getenv("SECRET_KEY")    # Pobranie klucza z tajnego miejsca
app.config['DATABASE'] =  os.getenv("DB_PATH")    # Pobranie sciezki do bazy danych


# __________________________________________________
#             ------- Kod Glowny -------
# __________________________________________________


# ------- Routes -------

@app.route('/')
def index():
    return render_template('templates/index.html', nav_active='index')


@app.route('/panel')
def panel():
    menu = Menu()
    menu.princik()
    return render_template('templates/base.html', nav_active='link')


# ------- Baza Danych -------

@app.teardown_appcontext
def close_db(error):
    '''Dekorator Flask do rejestrowania funkcji uzywanej przy zamknieciu aplikacji.\n
    Upewnia sie ze polaczenie z baza danych zostanie zamkniete.'''
    if hasattr(g, 'db'):
        g.db.close()

# ------- Pozostale -------

# Kompatybilnosc z uruchomieniem przez Python
if __name__ == '__main__':
    app.run()
