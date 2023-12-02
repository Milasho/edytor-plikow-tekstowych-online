# ------- Biblioteki -------
# Zewnetrzne biblioteki
from flask import Flask, flash, render_template
from flask import g 
from dotenv import load_dotenv
import sqlite3
import os

# Wewnetrzne biblioteki
from Pages.menu import Menu


# ------- Inicjalizacja Modulow -------
app = Flask(__name__)   # Instancja aplikacji Flask


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
    return render_template('index.html')


@app.route('/panel')
def panel():
    menu = Menu()
    menu.princik()
    return '<h1>aaaa</h1>'

# ------- Baza Danych -------

def get_db():
    '''Zwraca aktualne polaczenie do bazy danych'''

    if not hasattr(g, 'db'):  # Sprawdzenie czy polaczono
        # Zapisanie polaczenia w zmiennej globalnej (w jednym zadaniu)
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row  # Zwracane dane beda w postaci slownikow (unikniecie tuple)
    return g.db


@app.teardown_appcontext  # Dekorator Flask do rejestrowania funkcji uzywanej przy zamknieciu aplikacji
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

# ------- Pozostale -------

# Kompatybilnosc z uruchomieniem przez Python
if __name__ == '__main__':
    app.run()
