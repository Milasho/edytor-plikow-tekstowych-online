# ------- Biblioteki -------
# __________________________

# Zewnetrzne biblioteki
from flask import Flask, flash, render_template
import os
from dotenv import load_dotenv

# Wewnetrzne biblioteki
from Pages.menu import Menu

# ------- Konfiguracja -------
# ____________________________

app = Flask(__name__)   # Deklaracja aplikacji Flask
load_dotenv()   # Wczytanie zmiennych srodowiskowych z .env
app.config['SECRET_KEY'] =  os.getenv("SECRET_KEY")    # Pobranie klucza


# ------- Routes -------
# ______________________

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/panel')
def panel():
    menu = Menu()
    menu.princik()
    return '<h1>aaaa</h1>'

# ------- Pozostale -------
# _________________________

# Kompatybilnosc z uruchomieniem przez Python
if __name__ == '__main__':
    app.run()
