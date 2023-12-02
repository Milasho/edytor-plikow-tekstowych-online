# ------- Biblioteki -------
# __________________________

# Zewnetrzne biblioteki
from flask import Flask, flash, render_template
from dotenv import load_dotenv
import os

# Wewnetrzne biblioteki
from Pages.menu import Menu

# ------- Inicjalizacja Modulow -------
# _____________________________________

app = Flask(__name__)   # Instancja aplikacji Flask

# ------- Konfiguracja -------
# ____________________________

load_dotenv()   # Wczytanie zmiennych srodowiskowych z .env
app.config['SECRET_KEY'] =  os.getenv("SECRET_KEY")    # Pobranie klucza z tajnego miejsca


# __________________________________________________
#             ------- Kod Glowny -------
# __________________________________________________


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
