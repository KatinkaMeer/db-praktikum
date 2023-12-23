import sqlite3
import createdb

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

def create_KundenAccount(username, passwort, nachname, vorname, strasse, hausnummer, plz):
    executeUpdate("""
        INSERT INTO KundenAccount (Username, Passwort, Nachname, Vorname, Strasse, Hausnummer, Plz)
            VALUES(?, ?, ?, ?, ?, ?, ?)""",
        (username, passwort, nachname, vorname, strasse, hausnummer, plz)
    )

def update_KundenAccount(username, passwort, nachname, vorname, strasse, hausnummer, plz):
    executeUpdate("""
        INSERT OR REPLACE INTO KundenAccount (Username, Passwort, Nachname, Vorname, Strasse, Hausnummer, Plz)
            VALUES(?, ?, ?, ?, ?, ?, ?)""",
        (username, passwort, nachname, vorname, strasse, hausnummer, plz)
    )

def get_KundenAccount(username):
    request_pointer = getData("""
        SELECT Username, Passwort, Nachname, Vorname, Strasse, Hausnummer, Plz FROM KundenAccount
            WHERE Username= ? """,
        (username,))
    
    entry = request_pointer.fetchone()
    profil = {
            "username": entry[0],
            "password": entry[1],
            "firstname": entry[2],
            "lastname": entry[3],
            "street": entry[4],
            "housenumber": entry[5],
            "postalcode": entry[6]
        }

    return profil


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
    request_pointer = getData("""SELECT Username, Restaurantname, Beschreibung, Strasse, Hausnummer, Plz 
                              FROM GeschaeftsAccount""")
    for entry in request_pointer.fetchall():
        restaurant = {
            "username": entry[0],
            "name": entry[1],
            "description": entry[2],
            "street": entry[3],
            "housenumber": entry[4],
            "postalcode": entry[5]
        }
        restaurants.append(restaurant)
    return restaurants

def get_restaurants_near(username):
    restaurants = []
    request_pointer = getData("""SELECT GeschaeftsAccount.Username, Restaurantname, Beschreibung, GeschaeftsAccount.Strasse, GeschaeftsAccount.Hausnummer, GeschaeftsAccount.Plz 
                              FROM GeschaeftsAccount
                              INNER JOIN Lieferradius ON GeschaeftsAccount.Username = Lieferradius.GUsername
                              INNER JOIN KundenAccount ON Lieferradius.Plz = KundenACcount.Plz
                              WHERE KundenAccount.Username = ? """,(username,))
    for entry in request_pointer.fetchall():
        restaurant = {
            "username": entry[0],
            "name": entry[1],
            "description": entry[2],
            "street": entry[3],
            "housenumber": entry[4],
            "postalcode": entry[5]
        }
        restaurants.append(restaurant)
    return restaurants


def get_restaurant(username):
    request_pointer = getData("""SELECT Restaurantname, Beschreibung, Strasse, Hausnummer, Plz 
                              FROM GeschaeftsAccount
                              WHERE Username = ? """,(username,))
    result = request_pointer.fetchone()

    restaurant = {
            "name": result[0],
            "description": result[1],
            "street": result[2],
            "housenumber": result[3],
            "postalcode": result[4]
        }
    return restaurant

def get_items(username):
    items = []
    request_pointer = getData("""SELECT Restaurant, Name, Preis 
                              FROM Item
                              WHERE Restaurant = ? """, (username,))
    for entry in request_pointer.fetchall():
        restaurant = {
            "restaurant": entry[0],
            "name": entry[1],
            "price": entry[2],
        }
        items.append(restaurant)
    return items

def get_delivery_radius(username):
    postalcodes = []
    request_pointer = getData("""SELECT PLZ
                              FROM Lieferradius""")
    for entry in request_pointer.fetchall():
        postalcodes.append(entry[0])
    return postalcodes