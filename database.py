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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Oeffnungszeit(
            GUsername INTEGER NOT NULL,
            Wochentag INTEGER NOT NULL,
            Von time NOT NULL,
            Bis time NOT NULL,
            FOREIGN KEY (GUsername) REFERENCES GeschaeftsAccount(Username),
            PRIMARY KEY (GUsername, Wochentag)
        )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Item(
            Id INTEGER AUTO_INCREMENT NOT NULL,
            Restaurant INTEGER,
            Kategorie TEXT,
            Name TEXT,
            Preis INTEGER,
            PRIMARY KEY (Id),
            FOREIGN KEY (Restaurant) REFERENCES GeschaeftsAccount(username)
        )""")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Lieferradius(
            Plz INTEGER NOT NULL,
            GUsername INTEGER,
            FOREIGN KEY (GUsername) REFERENCES GeschaeftsAccount(Username),
            PRIMARY KEY (Plz, GUsername) 
        )""")
    
    cursor.execute("""
        INSERT or REPLACE INTO KundenAccount (Username, Passwort, Nachname, Vorname, Strasse, Hausnummer, Plz)
        VALUES ('edge', 'weiter', 'Pascal', 'Ritzenfeld', 'Engerweg', 6, 47877)
        """)
    
    cursor.execute("""
        INSERT or REPLACE INTO GeschaeftsAccount (Username, Passwort, Restaurantname, Beschreibung, Strasse, Hausnummer, Plz)
        VALUES ('pizza', 'weiter', 'pizzapalast', 'lecker Pizza', 'a', 1, 47877), 
                ('sushi', 'weiter', 'sushibar', 'lecker Sushi', 'a', 1, 47877)
        """)
    

    cursor.execute("""
        INSERT or REPLACE INTO Lieferradius (Plz, GUsername)
        VALUES (47877, 'pizza'), (47877, 'sushi')
        """)

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

def get_restaurants(username):
    restaurants = []
    request_pointer = getData("""SELECT Restaurantname, Beschreibung, GeschaeftsAccount.Strasse, GeschaeftsAccount.Hausnummer, GeschaeftsAccount.Plz 
                              FROM GeschaeftsAccount
                              INNER JOIN Lieferradius ON GeschaeftsAccount.Username = Lieferradius.GUsername
                              INNER JOIN KundenAccount ON Lieferradius.Plz = KundenACcount.Plz
                              WHERE KundenAccount.Username = ? """,(username,))
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