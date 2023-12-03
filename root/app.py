# ------- Biblioteki -------
# Zewnetrzne biblioteki
import sqlite3
import os
from flask import Flask, flash, url_for, render_template, redirect, g, request, session
from dotenv import load_dotenv

# Wewnetrzne biblioteki
from modules.db_utils import *
from modules.session_manager import UserPass
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
    return render_template('templates/index.html', active_navbar_part='index', logged=check_if_logged())
    
@app.route('/debug-login')
def logged_emulator():
    session['user'] = 'test'
    return render_template('templates/index.html', active_navbar_part='index', logged=True)

@app.route('/login', methods=['GET','POST'])
def login():
    # Zabezpieczenie przed proba polaczenia sie przez wpisanie adresu
    if check_if_logged() == True:
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('templates/login.html', active_navbar_part='login')
    else:
        user_name = '' if 'user_name' not in request.form else request.form['user_name']
        user_pass = '' if 'user_pass' not in request.form else request.form['user_pass']

        # Utworzenie obiektu na podstawie danych wpisanych przez uzytkownika
        login = UserPass(app, user_name, user_pass)

        # TODO: Refaktoryzacja sprawdzania credentiali ?
        # Weryfikacja uzytkownika 
        login_record = login.login_user()

        if login_record != None:
            session['user'] = user_name
            flash('Logowanie powiodło się, witaj: {}!'.format(user_name))
            return redirect(url_for('index'))
        else:
            flash('Logowanie nie powiodło się, spróbuj ponownie.')
            return render_template('templates/login.html', active_navbar_part='login')

@app.route('/logout')
def logout():
    if 'user' in session:  # Uzytkownik zalogowany w sesji
        session.pop('user', None)
        flash('Użytkownik został wylogowany')
    return redirect(url_for('index'))
    #return render_template('templates/index.html', active_navbar_part='index', logged=check_if_logged())

# ------- Baza Danych -------

@app.teardown_appcontext
def close_db(error):
    '''Upewnia sie ze polaczenie z baza danych zostanie zamkniete.'''
    # Uzywa Dekoratora Flask teardown_appcontext do rejestrowania funkcji uzywanej przy zamknieciu aplikacji.
    if hasattr(g, 'db'):
        g.db.close()

# ------- Pozostale -------

def check_if_logged():
    if 'user' in session:
        return True
    else:
        return False

# Kompatybilnosc z uruchomieniem przez Python
if __name__ == '__main__':
    app.run()
