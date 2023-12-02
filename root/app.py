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
    return render_template('templates/index.html', active_navbar_part='index')

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'GET':
        return render_template('templates/login.html', active_navbar_part='login')
    else:
        user_name = '' if 'user_name' not in request.form else request.form['user_name']
        user_pass = '' if 'user_pass' not in request.form else request.form['user_pass']

    login = UserPass(user_name, user_pass)
    login_record = login.login_user()

    if login_record != None:
        session['user'] = user_name
        flash('Logon succesfull, welcome {}'.format(user_name))
        return redirect(url_for('index'))
    else:
        flash('Logon failed, try again')
        return render_template('templates/login.html', active_navbar_part='login')

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
        flash('You are logged out')
    return redirect(url_for('teplates/login.html')) 

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
