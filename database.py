import sqlite3

def executeUpdate(sql, params = ()):
    dbcon = sqlite3.connect("instance/db.db")
    cursor = dbcon.cursor()
    cursor.execute(sql, params)
    dbcon.commit()
    cursor.close()
    dbcon.close()

def getData(sql, params = ()):
    dbcon = sqlite3.connect("instance/db.db")
    cursor = dbcon.cursor()
    cursor.execute(sql, params)
    return cursor

# SQLite3 Datatypes:
# NULL
# INTEGER
# REAL
# TEXT
# BLOB

def create_tables():
    dbcon = sqlite3.connect("instance/db.db")
    cursor = dbcon.cursor()
    
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS KundenAccount(
            Username TEXT PRIMARY KEY NOT NULL,
            Passwort TEXT NOT NULL,
            Nachname TEXT NOT NULL,
            Vorname TEXT NOT NULL,
            Strasse TEXT NOT NULL,
            Hausnummer INTEGER NOT NULL,
            Plz INTEGER NOT NULL
        )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS GeschaeftsAccount(
            Username TEXT PRIMARY KEY NOT NULL,
            Passwort TEXT NOT NULL,
            Restaurantname TEXT NOT NULL,
            Beschreibung TEST NOT NULL,
            Strasse TEXT NOT NULL,
            Hausnummer INTEGER NOT NULL,
            Plz INTEGER NOT NULL
        )""")

    #cursor.execute("""
    #    CREATE TABLE IF NOT EXISTS Restaurant(
    #        Id INTEGER AUTO_INCREMENT NOT NULL,
    #        Name TEXT,
    #        Beschreibung TEXT,
    #        PRIMARY KEY (Id)
    #    )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Oeffnungszeit(
            Rid INTEGER,
            Wochentag INTEGER,
            Von time,
            Bis time,
            PRIMARY KEY (Rid)
        )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Item(
            Id INTEGER AUTO_INCREMENT NOT NULL,
            Kategorie TEXT,
            Name TEXT,
            Preis INTEGER,
            PRIMARY KEY (Id) 
        )""")
    
    dbcon.commit()


def create_KundenAccount(username, passwort, nachname, vorname, strasse, hausnummer, plz):
    executeUpdate("""
        INSERT INTO KundenAccount (Username, Passwort, Nachname, Vorname, Strasse, Hausnummer, Plz)
            VALUES(?, ?, ?, ?, ?, ?, ?)""",
        (username, passwort, nachname, vorname, strasse, hausnummer, plz)
    )

def create_GeschaeftsAccount(username, passwort, resterauntname, beschreibung, strasse, hausnummer, plz):
    executeUpdate("""
        INSERT INTO GeschaeftsAccount (Username, Passwort, Restaurantname, Beschreibung, Strasse, Hausnummer, Plz)
            VALUES(?, ?, ?, ?, ?, ?, ?)""",
        (username, passwort, resterauntname, beschreibung, strasse, hausnummer, plz)
    )


def login_kunde(username, passwort):
    # Ergebnis des Vergleichs mit dem original pw aus db zum username
    request_pointer = getData("""SELECT Passwort FROM KundenAccount WHERE Username = ? """,(username,))
    
    result = request_pointer.fetchone()

    if result == None:
        return False
    
    origin_pw = result[0]
    return origin_pw == passwort

def login_geschaeft(username, passwort):
    # Ergebnis des Vergleichs mit dem original pw aus db zum username
    request_pointer = getData("""SELECT Passwort FROM GeschaeftsAccount WHERE Username = ? """,(username,))
    
    result = request_pointer.fetchone()

    if result == None:
        return False
    
    origin_pw = result[0]
    return origin_pw == passwort

def get_restaurants():
    restaurants = []
    request_pointer = getData("""SELECT Restaurantname, Beschreibung, Strasse, Hausnummer, Plz FROM GeschaeftsAccount""")
    for entry in request_pointer.fetchall():
        restaurant = {
            "name": entry[0],
            "description": entry[1],
            "street": entry[2],
            "housenumber": entry[3],
            "postalcode": entry[4]
        }
        restaurants.append(restaurant)
    return restaurants