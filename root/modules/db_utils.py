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

def get_file_id(username: str, file_name: str, app : Flask) -> int:
    """Uzyskaj id pliku z bazy danych na podstawie identyfikatora użytkownika i nazwy pliku.

    :param username: nazwa użytkownika.
    :param file_name: nazwa pliku.
    """

    if username is None or file_name is None:
        raise ValueError('Nieprawidłowe parametry')

    try:
        conn = get_db(app)
        cursor = conn.cursor()

        user_id = get_user_id(username=username, app=app)
        query = 'SELECT file_id FROM user_files WHERE user_id = ? AND file_name = ?'
        cursor.execute(query, (user_id, file_name))

        result = cursor.fetchone()
        file_id = result[0] if result else None  # Zwróć id pliku lub None, jeśli nie znaleziono
        conn.commit()
        return file_id
    finally:
        pass

def get_file_content_by_id(file_id, app : Flask):
    '''Pobierz zawartość pliku tekstowego z bazy danych na podstawie ID.
    :param file_id: id pliku odpowiadajace temu z bazy danych'''
    try:
        conn = get_db(app=app)
        cursor = conn.cursor()
        cursor.execute('SELECT content FROM user_files WHERE file_id = ?', (file_id,))
        file_content = cursor.fetchone()
        conn.commit()
        return file_content[0] if file_content else None  # Zwróć dane lub None, jeśli plik nie istnieje
    finally:
        pass

def get_files_with_ids(username: str, app : Flask) -> list:
    '''Pobiera listę plików wraz z ich identyfikatorami na podstawie nazwy użytkownika.'''
    try:
        conn = get_db(app)
        cursor = conn.cursor()
        
        query = '''
            SELECT file_id, file_name
            FROM user_files
            WHERE user_id = (SELECT user_id FROM users WHERE username = ?)
        '''
        cursor.execute(query, (username,))
        files_with_ids = [{'id': row['file_id'], 'filename': row['file_name']} for row in cursor.fetchall()]
        conn.commit()
        return files_with_ids
    finally:
        pass

def save_content_to_database(user_id, file_name, content, app):
    # TODO: Sprawdzanie slotow
    try:
        conn = get_db(app)
        cursor = conn.cursor()
        #content_text = content.encode('utf-8')

        cursor.execute('INSERT INTO user_files (user_id, file_name, content) VALUES (?, ?, ?)', (user_id, file_name, content))
        file_id = cursor.lastrowid  # Pobierz identyfikator nowo dodanego pliku
        conn.commit()
        return file_id
    finally:
        pass

def update_content_in_database(file_id, content, app):
    '''Aktualizuje treść pliku w bazie danych na podstawie ID pliku.'''
    try:
        print("DSFIJFUHDSFIUHDSFHUDSFH")
        conn = get_db(app)
        cursor = conn.cursor()
        cursor.execute('UPDATE user_files SET content = ? WHERE file_id = ?', (content, file_id))
        conn.commit()
    finally:
        pass

def get_user_id(username: str, app: Flask) -> int:
    """Pobierz id użytkownika na podstawie jego unikalnej nazwy.

    :param username: nazwa użytkownika.
    """
    try:
        conn = get_db(app)
        cursor = conn.cursor()
        query = 'SELECT user_id FROM users WHERE username = ?'
        cursor.execute(query, (username,))
        user_id_row = cursor.fetchone()
        conn.commit()
        if user_id_row is not None:
            user_id = user_id_row[0]  # Indeks 0, aby uzyskać pierwszą kolumnę (user_id)
            return int(user_id)
        else:
            # Obsługa przypadku, gdy użytkownik nie istnieje
            raise ValueError('Nieprawidłowe parametry')
    finally:
        pass

def get_available_slots(user_id, app: Flask):
    try:
        conn = get_db(app)
        cursor = conn.cursor()
        query = 'SELECT avaliable_slots FROM users WHERE user_id = ?'
        cursor.execute(query, (user_id,))
        avaliable_slots = cursor.fetchone()
        conn.commit()
        if avaliable_slots is not None:
            return int(avaliable_slots[0])
        else:
            # Obsługa przypadku, gdy użytkownik nie istnieje lub nie ma dostępnych slotów
            return 0
    finally:
        pass

def get_file_name_by_id(file_id, app: Flask):
    conn = get_db(app)
    cursor = conn.cursor()
    cursor.execute('SELECT file_name FROM user_files WHERE file_id = ?', (file_id,))
    file_name = cursor.fetchone()
    return file_name[0] if file_name else None

def user_is_owner(file_id, user_id, app):
    try:
        conn = get_db(app)
        cursor = conn.cursor()

        # Sprawdz czy użytkownik jest właścicielem pliku
        cursor.execute('SELECT user_id FROM user_files WHERE file_id = ?', (file_id,))
        result = cursor.fetchone()

        if result and result[0] == user_id:
            return True
        else:
            return False
    finally:
        pass

def delete_file_from_database(file_id, app):
    try:
        conn = get_db(app)
        cursor = conn.cursor()

        # Usuń plik z bazy danych
        cursor.execute('DELETE FROM user_files WHERE file_id = ?', (file_id,))
        conn.commit()
    finally:
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
