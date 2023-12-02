# Zewnetrzne biblioteki
from flask import Flask, flash, render_template
import os
from dotenv import load_dotenv

# Wewnetrzne biblioteki
from Pages.menu import Menu


app = Flask(__name__)   # Deklaracja aplikacji Flask
load_dotenv()   # Wczytanie zmiennych srodowiskowych z .env
app.config['SECRET_KEY'] =  os.getenv("SECRET_KEY")    # Pobranie klucza


# ------- Routes -------
# ______________________

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/main_menu')
def main_menu():
    menu = Menu()
    menu.princik()
    return '<h1>aaaa</h1>'


# Kompatybilnosc z uruchomieniem przez Python
if __name__ == '__main__':
    app.run()
