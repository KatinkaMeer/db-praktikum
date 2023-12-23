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
    
    ##creat etables

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
            GUsername TEXT NOT NULL,
            Wochentag TEXT NOT NULL CHECK(Wochentag IN ('Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag')),
            Von time NOT NULL,
            Bis time NOT NULL,
            FOREIGN KEY (GUsername) REFERENCES GeschaeftsAccount(Username),
            PRIMARY KEY (GUsername, Wochentag)
        )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Item(
            Restaurant INTEGER,
            Name TEXT,
            Kategorie TEXT,
            Preis INTEGER,
            PRIMARY KEY (Restaurant, Name)
            FOREIGN KEY (Restaurant) REFERENCES GeschaeftsAccount(username)
        )""")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Lieferradius(
            Plz INTEGER NOT NULL,
            GUsername TEXT NOT NULL,
            FOREIGN KEY (GUsername) REFERENCES GeschaeftsAccount(Username),
            PRIMARY KEY (Plz, GUsername) 
        )""")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Bestellung(
            KUsername TEXT NOT NULL,
            GUsername TEXT NOT NULL,
            Eingangszeit TEXT NOT NULL,
            Anmerkung TEXT,
            Bestellstatus TEXT NOT NULL CHECK( Bestellstatus IN ('in Bearbeitung','in Zubereitung','storniert','abgeschlossen') )
        )""")
    

    
    ##insert data
    
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
    
    cursor.execute("""
        INSERT or REPLACE INTO Item (Restaurant, Kategorie, Name, Preis)
        VALUES ('pizza', 'Hauptgericht', 'Pizza Salami', 750),
                ('pizza', 'Hauptgericht', 'Pizza Schinken', 750),
                ('pizza', 'Hauptgericht', 'Pizza Dreck', 750),
                ('sushi', 'Hauptgericht', 'Misosuppe', 750),
                ('sushi', 'Hauptgericht', 'Lachs Maki', 750)
        """)

    dbcon.commit()