# ------- Baza Danych -------

# Zewnetrzne biblioteki
from flask import Flask, g, session, render_template
import sqlite3

def get_db(app : Flask):
    '''Zwraca aktualne polaczenie do bazy danych'''

    if not hasattr(g, 'db'):  # Sprawdzenie czy polaczono
        # Zapisanie polaczenia w zmiennej globalnej (w jednym żądaniu)
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row  # Zwracane dane beda w postaci slownikow (unikniecie tuple)
    return g.db

def get_file_content_by_id(file_id):
    '''Pobierz zawartość pliku tekstowego z bazy danych na podstawie ID.
    :param file_id: id pliku odpowiadajace temu z bazy danych'''
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT content FROM files WHERE file_id = ?', (file_id,))
        file_content = cursor.fetchone()
        return file_content[0] if file_content else ''  # Zwróć zawartość lub pusty ciąg, jeśli plik nie istnieje
    finally:
        conn.close()

def get_file_id(username: str, slot_id: int) -> int:
    """Uzyskaj id pliku z bazy danych na podstawie unikalnej nazwy uzytkownika,
    oraz numeru slotu.

    :param username: nazwa uzytkownika.
    :param filename: the filename of uploaded image, optional.
    :param message: the warning message displayed to the user, optional.
    """
    pass


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
