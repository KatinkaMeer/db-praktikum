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
            ('mamamiapizza', '1234', 'Mamamia Pizza', 'Authentische italienische Pizza frisch aus einem Steinofen liefern wir direkt vor deine Haustür.', 'Hohe Straße', 7, 47051),
            ('zoesgrill', '1234', 'Zoes Grill', 'Wir präsentieren Ihnen leckere Rezepte mit Hackfleisch, Schafskäse, Lamm, Grillgemüse, Grillspießen und vielem mehr.', 'Königsberger Allee', 113, 47058),
            ('mcdaniels', '1234', 'McDaniels', 'Wir lieben es.', 'Portsmouthpl.', 1, 47051),
            ('subday', '1234', 'Subday', 'Esse frisch!', 'Königstraße', 48, 47051),
            ('kfp', '1234', 'KFP', 'Kentucky Fried Poultry', 'Königstraße', 56, 47051)
            ('sunsetgrill', '1234', 'Sunset Grill', 'Erleben Sie eine Symphonie der Aromen bei Sunset Grill. Unsere kulinarischen Kreationen sind eine Feier von Geschmack und Ambiente.', 'Sonnenallee', 30, 43040),
            ('fusiondelight', '1234', 'Fusion Delight', 'Tauchen Sie ein in die Welt der Fusion-Küche bei Fusion Delight. Unsere Köche verbinden verschiedene kulinarische Traditionen für ein delikates Geschmackserlebnis.', 'Mischstraße', 42, 41010),
            ('spicynoodlehouse', '1234', 'Spicy Noodle House', 'Bereiten Sie sich auf ein feuriges Fest bei Spicy Noodle House vor. Unsere Nudeln sind mit kühnen Gewürzen durchtränkt und entfachen Ihre Geschmacksknospen.', 'Feuerweg', 5, 46015),
            ('greenoasiscafe', '1234', 'Green Oasis Cafe', 'Entfliehen Sie bei Green Oasis Cafe dem Alltag. Genießen Sie unsere Garten-inspirierten Leckereien in einer ruhigen Umgebung.', 'Gartenweg', 12, 42030),
            ('stellarsteaks', '1234', 'Stellar Steaks', 'Gönnen Sie sich das Beste bei Stellar Steaks. Unsere erfahrenen Köche garantieren, dass jedes Steak ein Meisterwerk aus Geschmack und Zartheit ist.', 'Sterngasse', 8, 44025),
            ('thaiharmony', '1234', 'Thai Harmony', 'Entdecken Sie die perfekte Balance von süß, sauer und scharf bei Thai Harmony. Unsere authentischen Thai-Gerichte entführen Sie in die Straßen von Bangkok.', 'Siamstraße', 14, 48012),
            ('cocoacraze', '1234', 'Cocoa Craze', 'Befriedigen Sie Ihre süßen Gelüste bei Cocoa Craze. Unsere schokoladengetränkten Kreationen sind ein himmlisches Vergnügen für Schokoladenliebhaber.', 'Schokoladenplatz', 21, 45018),
            ('mysticalmezze', '1234', 'Mystical Mezze', 'Begleiten Sie uns auf eine Reise durch die mediterranen Aromen bei Mystical Mezze. Unsere kleinen Häppchen sind ein Fest der Geschmacksvielfalt und Tradition.', 'Olivengasse', 33, 49029),
            ('saffronspice', '1234', 'Saffron Spice', 'Erleben Sie die Reichhaltigkeit von Aromen bei Saffron Spice. Unsere Gerichte sind durchzogen von der Wärme und dem Duft des besten Safrans.', 'Gewürzweg', 9, 47036),
            ('tropicaltaco', '1234', 'Tropical Taco', 'Entfliehen Sie mit jedem Bissen zu einem tropischen Paradies bei Tropical Taco. Unsere Tacos sind eine Fiesta aus lebendigen Aromen und frischen Zutaten.', 'Palmenstraße', 17, 42044),
            ('zwiebelzirkus', '1234', 'Zwiebel Zirkus', 'Willkommen im Zwiebel Zirkus! Tauchen Sie ein in die Welt der Zwiebeln mit unseren raffinierten Gerichten, die diesen vielseitigen Geschmacksträger zelebrieren.', 'Zwiebelallee', 22, 42230),
            ('wurstundsenf', '1234', 'Wurst und Senf', 'Herzlich willkommen im Wurst und Senf! Genießen Sie traditionelle deutsche Wurstspezialitäten mit einer Auswahl an hausgemachten Senfsorten.', 'Senfplatz', 11, 42440),
            ('rheinweinhaus', '1234', 'Rhein Weinhaus', 'Entdecken Sie die Welt des deutschen Weins im Rhein Weinhaus. Unsere erlesene Auswahl an Weinen begleitet köstliche Gerichte, die die Region widerspiegeln.', 'Weinstraße', 29, 42650),
            ('schwarzbrotstube', '1234', 'Schwarzbrot Stube', 'Genießen Sie die Herzlichkeit einer deutschen Bäckerei in der Schwarzbrot Stube. Unsere Brote werden nach traditionellen Rezepten gebacken und begeistern jeden Brotliebhaber.', 'Brotgasse', 16, 42860),
            ('pilzparadies', '1234', 'Pilz Paradies', 'Tauchen Sie ein in das Pilz Paradies! Unsere Gerichte mit frischen Pilzen bieten eine kulinarische Reise durch die Wälder Deutschlands.', 'Waldweg', 8, 43070),
            ('sauerkrautundwurst', '1234', 'Sauerkraut und Wurst', 'Ein Fest für Liebhaber von Sauerkraut und Wurst! Erleben Sie die perfekte Kombination dieser traditionellen deutschen Delikatessen in unserem gemütlichen Lokal.', 'Sauergasse', 21, 43280),
            ('weisswurstwelt', '1234', 'Weisswurst Welt', 'Willkommen in der Weisswurst Welt! Kosten Sie die bayerische Delikatesse Weisswurst in verschiedenen Varianten, begleitet von traditionellen Beilagen.', 'Weißwurststraße', 14, 43490),
            ('schmalzundkraut', '1234', 'Schmalz und Kraut', 'Genießen Sie deftige Hausmannskost im Schmalz und Kraut. Unsere Gerichte mit Schmalz und Kraut sind ein Fest für den Gaumen und die Seele.', 'Schmalzweg', 25, 43700),
            ('pretzelparadies', '1234', 'Pretzel Paradies', 'Ein Paradies für Brezel-Liebhaber! Entdecken Sie im Pretzel Paradies eine Vielfalt von frisch gebackenen Brezeln in unterschiedlichen Geschmacksrichtungen.', 'Brezelallee', 17, 43910);      
        """)
    
    cursor.execute("""
        INSERT or REPLACE INTO Lieferradius (Plz, GUsername)
        VALUES (47877, 'mamamiapizza'), 
                (47877, 'sushiheaven')
        """)
    
    cursor.execute("""
        INSERT or REPLACE INTO Item (Restaurant, Kategorie, Name, Preis)
        VALUES ('pizza', 'Hauptgericht', 'Pizza Salami', 750),
                ('pizza', 'Hauptgericht', 'Pizza Schinken', 750),
                ('pizza', 'Hauptgericht', 'Pizza Dreck', 750),
                ('sushi', 'Hauptgericht', 'Misosuppe', 750),
                ('sushi', 'Hauptgericht', 'Lachs Maki', 750)
        """)

    cursor.execute("""
        INSERT or REPLACE INTO Bestellung (ROWID, KUsername, GUsername, Eingangszeit, Anmerkung, Bestellstatus)
        VALUES (1, 'edge', 'mamamiapizza', '19:45 Uhr', 'mit ohne alles', 'in Bearbeitung'),
            (2, 'edge', 'mamamiapizza', '19:00 Uhr', 'mit ohne alles', 'in Bearbeitung'),
            (3, 'edge', 'sushiheaven', '19:20 Uhr', 'mit ohne alles', 'in Bearbeitung')
        """)
    
    dbcon.commit()