import sqlite3
import createdb
import datetime

def executeUpdate(sql, params = ()):
    dbcon = sqlite3.connect("instance/db.db")
    cursor = dbcon.cursor()
    cursor.execute(sql, params)
    dbcon.commit()
    cursor.close()
    dbcon.close()
    return cursor.lastrowid

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
            "postalcode": entry[5],
        }
        restaurants.append(restaurant)
    return restaurants


def get_restaurant(username):
    request_pointer = getData("""SELECT Username, Restaurantname, Beschreibung, Strasse, Hausnummer, Plz 
                              FROM GeschaeftsAccount
                              WHERE Username = ? """,(username,))
    result = request_pointer.fetchone()

    restaurant = {
            "username": result[0],
            "name": result[1],
            "description": result[2],
            "street": result[3],
            "housenumber": result[4],
            "postalcode": result[5]
        }
    return restaurant

def get_items(username):
    items = []
    request_pointer = getData("""SELECT * 
                              FROM Item
                              WHERE Restaurant = ? AND Deaktiviert IS NULL
                              ORDER BY Kategorie DESC""", (username,))
    for entry in request_pointer.fetchall():
        restaurant = {
            "restaurant": entry[0],
            "name": entry[1],
            "category": entry[2],
            "price": entry[3]
        }
        items.append(restaurant)
    return items

def get_delivery_radius(username):
    postalcodes = []
    request_pointer = getData("""SELECT PLZ
                              FROM Lieferradius
                              WHERE GUsername = ? """, (username,))
    for entry in request_pointer.fetchall():
        postalcodes.append(entry[0])
    return postalcodes


def get_orders(username, business=False):
    query = """SELECT *
                FROM Bestellung
                WHERE KUsername = ?
                ORDER BY Eingangszeit DESC"""
                
    if business:
        query = """SELECT *
                FROM Bestellung
                WHERE GUsername = ?
                ORDER BY Eingangszeit DESC"""
    orders = []
    request_pointer = getData(query, (username,))
    for entry in request_pointer.fetchall():
        order = {
            "KUsername": entry[0],
            "GUsername": entry[1],
            "ordertime": entry[2],
            "comment": entry[3],
            "orderstatus": entry[4]
        }
        orders.append(order)
    return orders

def create_order(username: str, restaurant: str, items: list[dict], comment: str):
    timestamp = datetime.datetime.now()
    rowid = executeUpdate("""
        INSERT INTO Bestellung (KUsername, GUsername, Eingangszeit, Anmerkung, Bestellstatus)
        VALUES(?, ?, ?, ?, 'in Bearbeitung')""",
    (username, restaurant, timestamp, comment))
    
    for item in items:
        executeUpdate("""
            INSERT INTO bestellung_beinhaltet (Bestellung, Itemname, Menge)
            VALUES(?, ?, ?)""",
        (rowid, item["name"], item["amount"]))
    
def get_usernames(business=False) -> list:
    query = """SELECT Username
                FROM KundenAccount"""
                
    if business:
        query = """SELECT Username
                FROM GeschaeftsAccount"""

    request_pointer = getData(query)

    usernames = []
    for username in request_pointer.fetchall():
        usernames.append(username[0])

    return usernames