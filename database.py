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

def update_GeschaeftsAccount(username, passwort, resterauntname, beschreibung, strasse, hausnummer, plz):
    executeUpdate("""
        INSERT OR REPLACE INTO GeschaeftsAccount (Username, Passwort, Restaurantname, Beschreibung, Strasse, Hausnummer, Plz)
            VALUES(?, ?, ?, ?, ?, ?, ?)""",
        (username, passwort, resterauntname, beschreibung, strasse, hausnummer, plz)
    )

def update_items(restaurant, itemname, kategorie, beschreibung, preis, deaktiviert):
    executeUpdate("""
        INSERT OR REPLACE INTO Item (Restaurant, Name, Kategorie, IBeschreibung, Preis, Deaktiviert)
                  VALUES(?, ?, ?, ?, ?, ?)""",
        (restaurant, itemname, kategorie,  beschreibung, preis, deaktiviert)
    )

def update_lieferradius(plz,username):
    executeUpdate("""
        INSERT OR REPLACE INTO Item (Plz, Name)
                  VALUES(?, ?)""",
        (plz,username)
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

def get_restaurants_near_and_open(username, day):
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

        hours = get_business_hours_for(restaurant["username"], day)
        if hours:
            
            time = datetime.datetime.now().strftime("%H:%M") #Zeitstempel im Format Stunde(24):Minute

            #teile stunde und minute auf und caste zu int
            now_hour, now_min = [int(x) for x in time.split(":")]   
            start_hour, start_min = [int(x) for x in hours["from"].split(":")]
            end_hour, end_min = [int(x) for x in hours["until"].split(":")]

            if (now_hour == start_hour and now_min < start_min)\
            or (now_hour == end_hour and now_min >= end_min)\
            or (now_hour < start_hour or now_hour >= end_hour):
                continue
                
            
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
                              WHERE Restaurant = ? AND Deaktiviert = 0
                              ORDER BY Kategorie DESC""", (username,))
    for entry in request_pointer.fetchall():
        item = {
            "id": entry[0],
            "restaurant": entry[1],
            "name": entry[2],
            "category": entry[3],
            "description": entry[4],
            "price": entry[5],
            "deactivated": entry[6] 
        }
        items.append(item)
    return items

def get_item(id):
    request_pointer = getData("""SELECT *
                              FROM Item
                              WHERE ID = ? """,(id,))
    result = request_pointer.fetchone()

    item = {
            "id": result[0],
            "restaurant": result[1],
            "name": result[2],
            "category": result[3],
            "description": result[4],
            "price": result[5],
            "deactivated": result[6]
        }
    return item


def get_delivery_radius(username):
    postalcodes = []
    request_pointer = getData("""SELECT PLZ
                              FROM Lieferradius
                              WHERE GUsername = ? """, (username,))
    for entry in request_pointer.fetchall():
        postalcode = {
            "plz": entry[0]
        }
        postalcodes.append(postalcode)
    return postalcodes


def get_orders(username, business=False):
    orders = []
    request_pointer = getData(f"""
        SELECT rowid, *
        FROM Bestellung
        WHERE {'GUsername' if business else 'KUsername'} = ?
        ORDER BY Eingangszeit DESC""",
        (username,))
    
    for entry in request_pointer.fetchall():
        order = {
            "id": entry[0],
            "KUsername": entry[1],
            "GUsername": entry[2],
            "ordertime": entry[3],
            "comment": entry[4],
            "orderstatus": entry[5],
        }

        item_request_pointer = getData(f"""
            SELECT Item.ID, Item.Name, Item.Preis, bestellung_beinhaltet.Menge, Item.Kategorie, Item.IBeschreibung
            FROM bestellung_beinhaltet JOIN Item ON bestellung_beinhaltet.ItemID = Item.ID
            WHERE Bestellung = ?""",
            (order["id"],))

        order["items"] = []
        for x in item_request_pointer.fetchall():
            print(1)
            order["items"].append({
                "id": x[0],
                "name": x[1],
                "price": x[2],
                "amount": x[3],
                "category": x[4],
                "description": x[5],
            })
        orders.append(order)

    
    return orders

def create_order(username: str, restaurant: str, items: list[dict], comment: str):
    if not items: raise Exception('Es wurde eine leere Bestellung empfangen.')
    timestamp = datetime.datetime.now()
    rowid = executeUpdate("""
        INSERT INTO Bestellung (KUsername, GUsername, Eingangszeit, Anmerkung, Bestellstatus)
        VALUES(?, ?, ?, ?, 'in Bearbeitung')""",
    (username, restaurant, timestamp, comment))
    
    for item in items:
        executeUpdate("""
            INSERT OR ABORT INTO bestellung_beinhaltet (Bestellung, ItemID, Menge)
            VALUES(?, ?, ?)""",
        (rowid, item["id"], item["amount"]))
    
def get_usernames(business=False) -> list:

    request_pointer = getData(f"""
        SELECT Username
        FROM {'GeschaeftsAccount' if business else get_KundenAccount}""")

    usernames = []
    for username in request_pointer.fetchall():
        usernames.append(username[0])

    return usernames


def get_business_hours(username):
    times = {}
    request_pointer = getData("""
        SELECT *
        FROM Oeffnungszeit
        WHERE GUsername = ?""",
        (username,))
    
    for entry in request_pointer.fetchall():
        times[entry[1]] = {
            "from": entry[2],
            "until": entry[3],
        }
    return times

def get_business_hours_for(username, day):
    request_pointer = getData("""
        SELECT *
        FROM Oeffnungszeit
        WHERE GUsername = ? AND Wochentag = ?""",
        (username, day))
    entry = request_pointer.fetchone()
    result = None
    if entry:
        result = {
            "restaurant": entry[0],
            "day": entry[1],
            "from": entry[2],
            "until": entry[3],
        }
    return result
    
def update_orderstatus(orderid: int, status: str):
    executeUpdate("""
        UPDATE Bestellung
        SET Bestellstatus = ?
        WHERE rowid == ?
        """, (status, orderid))