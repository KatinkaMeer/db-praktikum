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
        VALUES ('cafebluerose', '1234', 'Café Blue Rose', 'Café blue rose ist ein kleines, ruhiges Café in der Innenstadt. Unsere selbstgemachten Kuchen schmecken klein und groß.', 'Königstraße', 25, 46735), 
            ('sushiheaven', '1234', 'Sushi Heaven', 'Unsere Sushi- Meister, trainiert in Japan, zaubern euch authentisches Sushi.', 'Oststraße', 16, 45545),
            ('bowl', '1234', 'Bowl', 'Wir verkaufen verschiedene Bowls. Ihr könnt hier auch eigene Bowls zusammenstellen!', 'Landstraße', 165, 46323),
            ('americasstory', '1234', 'Americas Story', 'Das Konzept unseres Restaurants ist es die Geschichte Amerikas durch das Essen neu zu erleben.', 'An den Buchen', 18, 45432),
            ('sidebysoups', '1234', 'Side by Soups', 'Bei uns bekommst du Suppen aller Art. Unsere Rezepte kommen aus der ganzen Welt.', 'Ring des Lebens', 66, 49736),
            ('mamamiapizza', '1234', 'Mamamia Pizza', 'Authentische italienische Pizza frisch aus einem Steinofen liefern wir direkt vor deine Haustür.', 'Hohe Str.', 7, 47051),
            ('zoesgrill', '1234', 'Zoes Grill', 'Wir präsentieren Ihnen leckere Rezepte mit Hackfleisch, Schafskäse, Lamm, Grillgemüse, Grillspießen und vielem mehr.', 'Königsberger Allee', 113, 47058),
            ('mcdaniels', '1234', 'McDaniels', 'Wir lieben es.', 'Portsmouthpl.', 1, 47051),
            ('subday', '1234', 'Subday', 'Esse frisch!', 'Königstraße', 48, 47051),
            ('kfp', '1234', 'KFP', 'Kentucky Fried Poultry', 'Königstraße', 56, 47051)
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