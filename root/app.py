# ------- Biblioteki -------
# Zewnetrzne biblioteki
import sqlite3
import os
from flask import Flask, flash, render_template
from flask import g 
from dotenv import load_dotenv

# Wewnetrzne biblioteki
import modules.db_utils
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
    return render_template('templates/index.html')


@app.route('/panel')
def panel():
    menu = Menu()
    menu.princik()
    return '<h1>aaaa</h1>'


# ------- Baza Danych -------

@app.teardown_appcontext  # Dekorator Flask do rejestrowania funkcji uzywanej przy zamknieciu aplikacji
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

# ------- Pozostale -------

# Kompatybilnosc z uruchomieniem przez Python
if __name__ == '__main__':
    app.run()
