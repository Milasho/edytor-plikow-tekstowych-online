# ------- Baza Danych -------

# Zewnetrzne biblioteki
from flask import Flask,g, render_template
import sqlite3

def get_db(app : Flask):
    '''Zwraca aktualne polaczenie do bazy danych'''

    if not hasattr(g, 'db'):  # Sprawdzenie czy polaczono
        # Zapisanie polaczenia w zmiennej globalnej (w jednym zadaniu)
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row  # Zwracane dane beda w postaci slownikow (unikniecie tuple)
    return g.db

def _send_record_to_db_exapmle(app : Flask):
    '''Przykladowa funkcja do wysylania danych do bazy danych'''
    x,y,z = 1
    db = get_db(app)
    sql_command = 'insert into costam(1x, 1y, 1z) values(?, ?, ?)'
    db.execute(sql_command, [x, y, z])
    db.commit()

def _receive_record_to_db_exapmle(app : Flask):
    '''Przykladowa funkcja do pobrania danych z bazy danych'''
    db = get_db(app)
    sql_command= 'select id, 1x, 1y from costam'
    cur = db.execute(sql_command)  # kursor pozwala odczytac dane przez zapytanie
    costam = cur.fetchall()  # Rekordy zostana zapisane do obiektu costam, ktory jest zbiorem slownikow
    return render_template('text.html', tabela=costam)
