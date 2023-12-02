# ------- Baza Danych -------

# Zewnetrzne biblioteki
from flask import g 
import sqlite3

def get_db():
    '''Zwraca aktualne polaczenie do bazy danych'''

    if not hasattr(g, 'db'):  # Sprawdzenie czy polaczono
        # Zapisanie polaczenia w zmiennej globalnej (w jednym zadaniu)
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row  # Zwracane dane beda w postaci slownikow (unikniecie tuple)
    return g.db

def send_record_to_db_exapmle():
    x,y,z = 1
    db = get_db()
    sql_command = 'insert into costam(1x, 1y, 1z) values(?, ?, ?)'
    db.execute(sql_command, [x, y, z])
    db.commit()
