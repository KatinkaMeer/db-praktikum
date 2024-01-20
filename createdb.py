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
            Bis time NOT NULL CHECK(Von < Bis),
            FOREIGN KEY (GUsername) REFERENCES GeschaeftsAccount(Username),
            PRIMARY KEY (GUsername, Wochentag)
        )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Item(
            ID INTEGER NOT NULL,
            Restaurant INTEGER,
            Name TEXT,
            Kategorie TEXT,
            IBeschreibung TEXT,
            Preis INTEGER,
            Deaktiviert INTEGER DEFAULT 0 CHECK(Deaktiviert IN (0, 1)),
            PRIMARY KEY (ID),
            FOREIGN KEY (Restaurant) REFERENCES GeschaeftsAccount(username),
            UNIQUE(Restaurant, Name, Kategorie, IBeschreibung, Preis)                   
        );""")
    
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS deactivate_item
        BEFORE INSERT ON Item
        WHEN EXISTS(SELECT * FROM bestellung_beinhaltet WHERE ItemID = New.ID)
        BEGIN
        UPDATE Item SET Deaktiviert = 1
        WHERE Restaurant = New.Restaurant AND Name = New.Name;
        END;
        """)
    
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS delete_item
        BEFORE INSERT ON Item
        WHEN NOT EXISTS(SELECT * FROM bestellung_beinhaltet WHERE ItemID = New.ID)
        BEGIN
        DELETE FROM Item
        WHERE Restaurant = New.Restaurant AND Name = New.Name;
        END;
        """)

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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bestellung_beinhaltet(
            Bestellung INTEGER NOT NULL,
            ItemID INTEGER NOT NULL,
            Menge INTEGER NOT NULL,
            FOREIGN KEY(Bestellung) REFERENCES Bestellung(ID)
            FOREIGN KEY(ItemID) REFERENCES Item(ID) ON DELETE CASCADE
        )""")
    
    
    ##insert data
    
    cursor.execute("""
        INSERT or REPLACE INTO KundenAccount (Username, Passwort, Nachname, Vorname, Strasse, Hausnummer, Plz)
        VALUES ('edge', 'weiter', 'Pascal', 'Ritzenfeld', 'Engerweg', 6, 47877)
        """)
    
    cursor.execute("""
        INSERT or REPLACE INTO GeschaeftsAccount (Username, Passwort, Restaurantname, Beschreibung, Strasse, Hausnummer, Plz)
        VALUES ('cafebluerose', '1234', 'Café Blue Rose', 'Café blue rose ist ein kleines, ruhiges Café in der Innenstadt. Unsere selbstgemachten Kuchen schmecken Klein und Groß.', 'Königstraße', 25, 46735), 
            ('sushiheaven', '1234', 'Sushi Heaven', 'Unsere Sushi- Meister, trainiert in Japan, zaubern euch authentisches Sushi.', 'Oststraße', 16, 45545),
            ('bowl', '1234', 'Bowl', 'Wir verkaufen verschiedene Bowls. Ihr könnt hier auch eigene Bowls zusammenstellen!', 'Landstraße', 165, 46323),
            ('americanstory', '1234', 'American Story', 'Das Konzept unseres Restaurants ist es die Geschichte Amerikas durch das Essen neu zu erleben.', 'An den Buchen', 18, 45432),
            ('sidebysoups', '1234', 'Side by Soups', 'Bei uns bekommst du Suppen aller Art. Unsere Rezepte kommen aus der ganzen Welt.', 'Ring des Lebens', 66, 49736),
            ('mamamiapizza', '1234', 'Mamamia Pizza', 'Authentische italienische Pizza frisch aus einem Steinofen liefern wir direkt vor deine Haustür.', 'Hohe Straße', 7, 47051),
            ('zoesgrill', '1234', 'Zoes Grill', 'Wir präsentieren Ihnen leckere Rezepte mit Hackfleisch, Schafskäse, Lamm, Grillgemüse, Grillspießen und vielem mehr.', 'Königsberger Allee', 113, 47058),
            ('mcdaniels', '1234', 'McDaniels', 'Wir lieben es.', 'Portsmouthpl.', 1, 47051),
            ('subday', '1234', 'Subday', 'Iss frisch!', 'Königstraße', 48, 47051),
            ('kfp', '1234', 'KFP', 'Kentucky Fried Poultry', 'Königstraße', 56, 47051),
            ('sunsetgrill', '1234', 'Sunset Grill', 'Erleben Sie eine Symphonie der Aromen bei Sunset Grill. Unsere kulinarischen Kreationen sind eine Feier von Geschmack und Ambiente.', 'Sonnenallee', 30, 45545),
            ('fusiondelight', '1234', 'Fusion Delight', 'Tauchen Sie ein in die Welt der Fusion-Küche bei Fusion Delight. Unsere Köche verbinden verschiedene kulinarische Traditionen für ein delikates Geschmackserlebnis.', 'Mischstraße', 42, 45545),
            ('spicynoodlehouse', '1234', 'Spicy Noodle House', 'Bereiten Sie sich auf ein feuriges Fest bei Spicy Noodle House vor. Unsere Nudeln sind mit kühnen Gewürzen durchtränkt und entfachen Ihre Geschmacksknospen.', 'Feuerweg', 5, 45545),
            ('greenoasiscafe', '1234', 'Green Oasis Cafe', 'Entfliehen Sie bei Green Oasis Cafe dem Alltag. Genießen Sie unsere Garten-inspirierten Leckereien in einer ruhigen Umgebung.', 'Gartenweg', 12, 45545),
            ('stellarsteaks', '1234', 'Stellar Steaks', 'Gönnen Sie sich das Beste bei Stellar Steaks. Unsere erfahrenen Köche garantieren, dass jedes Steak ein Meisterwerk aus Geschmack und Zartheit ist.', 'Sterngasse', 8, 45545),
            ('thaiharmony', '1234', 'Thai Harmony', 'Entdecken Sie die perfekte Balance von süß, sauer und scharf bei Thai Harmony. Unsere authentischen Thai-Gerichte entführen Sie in die Straßen von Bangkok.', 'Siamstraße', 14, 45545),
            ('cocoacraze', '1234', 'Cocoa Craze', 'Befriedigen Sie Ihre süßen Gelüste bei Cocoa Craze. Unsere schokoladengetränkten Kreationen sind ein himmlisches Vergnügen für Schokoladenliebhaber.', 'Schokoladenplatz', 21, 45545),
            ('mysticalmezze', '1234', 'Mystical Mezze', 'Begleiten Sie uns auf eine Reise durch die mediterranen Aromen bei Mystical Mezze. Unsere kleinen Häppchen sind ein Fest der Geschmacksvielfalt und Tradition.', 'Olivengasse', 33, 45545),
            ('saffronspice', '1234', 'Saffron Spice', 'Erleben Sie die Reichhaltigkeit von Aromen bei Saffron Spice. Unsere Gerichte sind durchzogen von der Wärme und dem Duft des besten Safrans.', 'Gewürzweg', 9, 45545),
            ('tropicaltaco', '1234', 'Tropical Taco', 'Entfliehen Sie mit jedem Bissen zu einem tropischen Paradies bei Tropical Taco. Unsere Tacos sind eine Fiesta aus lebendigen Aromen und frischen Zutaten.', 'Palmenstraße', 17, 45545),
            ('zwiebelzirkus', '1234', 'Zwiebel Zirkus', 'Willkommen im Zwiebel Zirkus! Tauchen Sie ein in die Welt der Zwiebeln mit unseren raffinierten Gerichten, die diesen vielseitigen Geschmacksträger zelebrieren.', 'Zwiebelallee', 22, 45545),
            ('wurstundsenf', '1234', 'Wurst und Senf', 'Herzlich willkommen im Wurst und Senf! Genießen Sie traditionelle deutsche Wurstspezialitäten mit einer Auswahl an hausgemachten Senfsorten.', 'Senfplatz', 11, 45545),
            ('rheinweinhaus', '1234', 'Rhein Weinhaus', 'Entdecken Sie die Welt des deutschen Weins im Rhein Weinhaus. Unsere erlesene Auswahl an Weinen begleitet köstliche Gerichte, die die Region widerspiegeln.', 'Weinstraße', 29, 45545),
            ('schwarzbrotstube', '1234', 'Schwarzbrot Stube', 'Genießen Sie die Herzlichkeit einer deutschen Bäckerei in der Schwarzbrot Stube. Unsere Brote werden nach traditionellen Rezepten gebacken und begeistern jeden Brotliebhaber.', 'Brotgasse', 16, 45545),
            ('pilzparadies', '1234', 'Pilz Paradies', 'Tauchen Sie ein in das Pilz Paradies! Unsere Gerichte mit frischen Pilzen bieten eine kulinarische Reise durch die Wälder Deutschlands.', 'Waldweg', 8, 45545),
            ('sauerkrautundwurst', '1234', 'Sauerkraut und Wurst', 'Ein Fest für Liebhaber von Sauerkraut und Wurst! Erleben Sie die perfekte Kombination dieser traditionellen deutschen Delikatessen in unserem gemütlichen Lokal.', 'Sauergasse', 21, 45545);
            """)
    
    cursor.execute("""
        INSERT or REPLACE INTO Lieferradius (Plz, GUsername)
        VALUES (47877, 'mamamiapizza'), 
                (47877, 'sushiheaven'),
                (47877, 'cafebluerose'),
                (47877, 'bowl'),
                (47877, 'americasstory'),
                (47877, 'sidebysoups'),
                (47877, 'zoesgrill'),
                (47877, 'mcdaniels'),
                (47877, 'subday'),
                (47877, 'kfp'),
                (47877, 'sunsetgrill'),
                (47877, 'fusiondelight'),
                (47877, 'spicynoodlehouse'),
                (47877, 'greenoasiscafe'),
                (47877, 'stellarsteaks'),
                (47877, 'thaiharmony'),
                (47877, 'cocoacraze'),
                (47877, 'mysticalmezze'),
                (47877, 'saffronspice'),
                (47877, 'tropicaltaco'),
                (47877, 'zwiebelzirkus'),
                (47877, 'wurstundsenf'),
                (47877, 'rheinweinhaus'),
                (47877, 'schwarzbrotstube'),
                (47877, 'pilzparadies'),
                (47877, 'sauerkrautundwurst'),
                (47877, 'weisswurstwelt'),
                (47877, 'schmalzundkraut'),
                (47877, 'pretzelparadies');
        """)
    
    cursor.execute("""
        INSERT or REPLACE INTO Item (Restaurant, Kategorie, Name, Preis)
        VALUES ('mamamiapizza', 'Vorspeise', 'Bruschetta', 550),
            ('mamamiapizza', 'Vorspeise', 'Caprese-Salat', 650),
            ('mamamiapizza', 'Vorspeise', 'Knoblauchbrot', 500),
            ('mamamiapizza', 'Vorspeise', 'Antipasti-Platte', 850),
            ('mamamiapizza', 'Hauptgericht', 'Pizza Margherita', 750),
            ('mamamiapizza', 'Hauptgericht', 'Pizza Quattro Formaggi', 800),
            ('mamamiapizza', 'Hauptgericht', 'Pasta Bolognese', 700),
            ('mamamiapizza', 'Hauptgericht', 'Lasagne al Forno', 850),
            ('mamamiapizza', 'Hauptgericht', 'Risotto Funghi', 780),
            ('mamamiapizza', 'Hauptgericht', 'Calzone', 820),
            ('mamamiapizza', 'Hauptgericht', 'Gnocchi Gorgonzola', 750),
            ('mamamiapizza', 'Hauptgericht', 'Penne all Arrabbiata', 720),
            ('mamamiapizza', 'Hauptgericht', 'Linguine ai Frutti di Mare', 890),
            ('mamamiapizza', 'Dessert', 'Tiramisu', 550),
            ('mamamiapizza', 'Dessert', 'Panna Cotta', 600),
            ('mamamiapizza', 'Getränk', 'Limonata', 350),
            ('mamamiapizza', 'Getränk', 'Aranciata', 350),
            ('mamamiapizza', 'Getränk', 'Pellegrino', 400),
            ('mamamiapizza', 'Getränk', 'Acqua Minerale', 300),
                   
            ('sushiheaven', 'Vorspeise', 'Edamame', 450),
            ('sushiheaven', 'Vorspeise', 'Gyoza', 600),
            ('sushiheaven', 'Vorspeise', 'Agedashi Tofu', 550),
            ('sushiheaven', 'Vorspeise', 'Wakame Salat', 500),
            ('sushiheaven', 'Hauptgericht', 'Sushi Mix', 800),
            ('sushiheaven', 'Hauptgericht', 'Sashimi Teller', 850),
            ('sushiheaven', 'Hauptgericht', 'Tempura Udon', 750),
            ('sushiheaven', 'Hauptgericht', 'Chirashi Bowl', 820),
            ('sushiheaven', 'Hauptgericht', 'Dragon Roll', 780),
            ('sushiheaven', 'Hauptgericht', 'Rainbow Roll', 880),
            ('sushiheaven', 'Hauptgericht', 'Unagi Don', 900),
            ('sushiheaven', 'Hauptgericht', 'Yakitori Spieße', 720),
            ('sushiheaven', 'Hauptgericht', 'Sushi Burger', 850),
            ('sushiheaven', 'Dessert', 'Matcha Eis', 500),
            ('sushiheaven', 'Dessert', 'Mochi', 550),
            ('sushiheaven', 'Getränk', 'Grüner Tee', 300),
            ('sushiheaven', 'Getränk', 'Sake', 600),
            ('sushiheaven', 'Getränk', 'Ramune', 350),
            ('sushiheaven', 'Getränk', 'Lychee Eistee', 400),
                   
            ('bowl', 'Vorspeise', 'Edamame Bowl', 550),
            ('bowl', 'Vorspeise', 'Avocado Hummus', 600),
            ('bowl', 'Vorspeise', 'Kimchi Pfannkuchen', 500),
            ('bowl', 'Vorspeise', 'Thai Sommerrollen', 650),
            ('bowl', 'Hauptgericht', 'Teriyaki Hähnchen Bowl', 750),
            ('bowl', 'Hauptgericht', 'Vegetarische Buddha Bowl', 800),
            ('bowl', 'Hauptgericht', 'Poke Bowl', 700),
            ('bowl', 'Hauptgericht', 'Ramen Suppe', 850),
            ('bowl', 'Hauptgericht', 'Burrito Bowl', 780),
            ('bowl', 'Hauptgericht', 'Süßkartoffel Quinoa Bowl', 820),
            ('bowl', 'Hauptgericht', 'Couscous Gemüse Bowl', 750),
            ('bowl', 'Hauptgericht', 'Thai Glasnudelsalat', 720),
            ('bowl', 'Dessert', 'Matcha Cheesecake', 550),
            ('bowl', 'Dessert', 'Ananas Kokosnuss Sorbet', 600),
            ('bowl', 'Getränk', 'Ingwer Limonade', 350),
            ('bowl', 'Getränk', 'Aloe Vera Getränk', 350),
            ('bowl', 'Getränk', 'Matcha Latte', 400),
            ('bowl', 'Getränk', 'Chai Tee', 300),
                   
            ('americasstory', 'Vorspeise', 'Nachos mit Guacamole', 600),
            ('americasstory', 'Vorspeise', 'Chicken Wings', 650),
            ('americasstory', 'Vorspeise', 'Quesadillas', 550),
            ('americasstory', 'Vorspeise', 'Spinat Artischocken Dip', 700),
            ('americasstory', 'Hauptgericht', 'Burger "The American"', 800),
            ('americasstory', 'Hauptgericht', 'BBQ Ribs', 850),
            ('americasstory', 'Hauptgericht', 'Mac n Cheese', 700),
            ('americasstory', 'Hauptgericht', 'Steak Tacos', 900),
            ('americasstory', 'Hauptgericht', 'Cajun Hähnchen', 780),
            ('americasstory', 'Hauptgericht', 'Jambalaya', 820),
            ('americasstory', 'Hauptgericht', 'Shrimp Po Boy Sandwich', 750),
            ('americasstory', 'Dessert', 'New York Cheesecake', 650),
            ('americasstory', 'Dessert', 'Pecan Pie', 700),
            ('americasstory', 'Getränk', 'Root Beer', 350),
            ('americasstory', 'Getränk', 'Mint Julep', 400),
            ('americasstory', 'Getränk', 'Arnold Palmer', 300),
            ('americasstory', 'Getränk', 'Southern Sweet Tea', 350),
            
            ('sidebysoups', 'Vorspeise', 'Tomatensuppe', 550),
            ('sidebysoups', 'Vorspeise', 'Minestrone', 600),
            ('sidebysoups', 'Vorspeise', 'Gazpacho', 500),
            ('sidebysoups', 'Vorspeise', 'Linsensuppe', 650),
            ('sidebysoups', 'Hauptgericht', 'Hühnersuppe', 750),
            ('sidebysoups', 'Hauptgericht', 'Ramen Suppe', 800),
            ('sidebysoups', 'Hauptgericht', 'Pho', 700),
            ('sidebysoups', 'Hauptgericht', 'Chowder', 850),
            ('sidebysoups', 'Hauptgericht', 'Gulaschsuppe', 780),
            ('sidebysoups', 'Hauptgericht', 'Miso Ramen', 820),
            ('sidebysoups', 'Hauptgericht', 'Kürbissuppe', 750),
            ('sidebysoups', 'Dessert', 'Schokoladenmousse', 550),
            ('sidebysoups', 'Dessert', 'Tiramisu', 600),
            ('sidebysoups', 'Getränk', 'Eistee', 350),
            ('sidebysoups', 'Getränk', 'Frisch gepresster Saft', 400),
            ('sidebysoups', 'Getränk', 'Ingwer-Zitronen-Tee', 300),
            ('sidebysoups', 'Getränk', 'Gemüsesaft', 350),

            ('zoesgrill', 'Vorspeise', 'Falafel', 550),
            ('zoesgrill', 'Vorspeise', 'Hummus mit Pitabrot', 600),
            ('zoesgrill', 'Vorspeise', 'Baba Ganoush', 500),
            ('zoesgrill', 'Vorspeise', 'Taboulé Salat', 650),
            ('zoesgrill', 'Hauptgericht', 'Souvlaki Spieße', 750),
            ('zoesgrill', 'Hauptgericht', 'Moussaka', 800),
            ('zoesgrill', 'Hauptgericht', 'Gyros Teller', 700),
            ('zoesgrill', 'Hauptgericht', 'Shawarma Wrap', 850),
            ('zoesgrill', 'Hauptgericht', 'Ratatouille', 780),
            ('zoesgrill', 'Hauptgericht', 'Linsen-Kofta Burger', 820),
            ('zoesgrill', 'Hauptgericht', 'Gemüse-Satay Spieße', 750),
            ('zoesgrill', 'Dessert', 'Baklava', 550),
            ('zoesgrill', 'Dessert', 'Loukoumades', 600),
            ('zoesgrill', 'Getränk', 'Ouzo', 350),
            ('zoesgrill', 'Getränk', 'Türkischer Kaffee', 400),
            ('zoesgrill', 'Getränk', 'Ayran', 300),
            ('zoesgrill', 'Getränk', 'Granatapfelsaft', 350),

            ('mcdaniels', 'Vorspeise', 'Chicken Nuggets', 550),
            ('mcdaniels', 'Vorspeise', 'Mozerella Sticks', 600),
            ('mcdaniels', 'Vorspeise', 'Nachos mit Käsesauce', 500),
            ('mcdaniels', 'Vorspeise', 'Wings mit BBQ Sauce', 650),
            ('mcdaniels', 'Hauptgericht', 'Big McD Burger', 750),
            ('mcdaniels', 'Hauptgericht', 'Crispy Chicken Burger', 800),
            ('mcdaniels', 'Hauptgericht', 'Filet-O-Fish', 700),
            ('mcdaniels', 'Hauptgericht', 'McWrap Caesar', 850),
            ('mcdaniels', 'Hauptgericht', 'McVeggie Burger', 780),
            ('mcdaniels', 'Hauptgericht', 'McChicken', 820),
            ('mcdaniels', 'Hauptgericht', 'Double Cheeseburger', 750),
            ('mcdaniels', 'Dessert', 'Apfeltasche', 550),
            ('mcdaniels', 'Dessert', 'McFlurry mit Oreo', 600),
            ('mcdaniels', 'Getränk', 'Cola', 350),
            ('mcdaniels', 'Getränk', 'Eistee Pfirsich', 400),
            ('mcdaniels', 'Getränk', 'Milchshake Erdbeere', 300),
            ('mcdaniels', 'Getränk', 'Sprite', 350),

            ('subday', 'Vorspeise', 'Knoblauchbrot', 550),
            ('subday', 'Vorspeise', 'Caprese Salat', 600),
            ('subday', 'Vorspeise', 'Chicken Wings', 500),
            ('subday', 'Vorspeise', 'Nachos mit Käse', 650),
            ('subday', 'Hauptgericht', 'Italian BMT Sub', 750),
            ('subday', 'Hauptgericht', 'Chicken Teriyaki Sub', 800),
            ('subday', 'Hauptgericht', 'Veggie Delight Sub', 700),
            ('subday', 'Hauptgericht', 'Tuna Sub', 850),
            ('subday', 'Hauptgericht', 'Steak and Cheese Sub', 780),
            ('subday', 'Hauptgericht', 'Turkey and Bacon Ranch Melt', 820),
            ('subday', 'Hauptgericht', 'Spicy Italian Sub', 750),
            ('subday', 'Dessert', 'Chocolate Chip Cookie', 550),
            ('subday', 'Dessert', 'White Chocolate Macadamia Nut Cookie', 600),
            ('subday', 'Getränk', 'Pepsi', 350),
            ('subday', 'Getränk', 'Mountain Dew', 400),
            ('subday', 'Getränk', 'Lipton Iced Tea', 300),
            ('subday', 'Getränk', 'Aquafina Wasser', 350),
                   
            ('kfp', 'Vorspeise', 'Egg Rolls', 550),
            ('kfp', 'Vorspeise', 'Crab Rangoon', 600),
            ('kfp', 'Vorspeise', 'Hot and Sour Suppe', 500),
            ('kfp', 'Vorspeise', 'Edamame', 650),
            ('kfp', 'Hauptgericht', 'General Tsos Chicken', 750),
            ('kfp', 'Hauptgericht', 'Sweet and Sour Pork', 800),
            ('kfp', 'Hauptgericht', 'Beef and Broccoli', 700),
            ('kfp', 'Hauptgericht', 'Kung Pao Shrimp', 850),
            ('kfp', 'Hauptgericht', 'Vegetable Lo Mein', 780),
            ('kfp', 'Hauptgericht', 'Mongolian Beef', 820),
            ('kfp', 'Hauptgericht', 'Szechuan Chicken', 750),
            ('kfp', 'Dessert', 'Fortune Cookies', 550),
            ('kfp', 'Dessert', 'Almond Cookies', 600),
            ('kfp', 'Getränk', 'Jasmin Tee', 350),
            ('kfp', 'Getränk', 'Lychee Limonade', 400),
            ('kfp', 'Getränk', 'Plum Wine', 300),
            ('kfp', 'Getränk', 'Sake', 350),
                   
            ('sunsetgrill', 'Vorspeise', 'Spinat-Artischocken-Dip', 550),
            ('sunsetgrill', 'Vorspeise', 'Mozzarella-Sticks', 600),
            ('sunsetgrill', 'Vorspeise', 'Chicken Quesadilla', 500),
            ('sunsetgrill', 'Vorspeise', 'Nachos Supreme', 650),
            ('sunsetgrill', 'Hauptgericht', 'Sunset Burger', 750),
            ('sunsetgrill', 'Hauptgericht', 'Ribeye-Steak', 800),
            ('sunsetgrill', 'Hauptgericht', 'Lachsfilet', 700),
            ('sunsetgrill', 'Hauptgericht', 'Chicken Alfredo Pasta', 850),
            ('sunsetgrill', 'Hauptgericht', 'Vegetarische Fajitas', 780),
            ('sunsetgrill', 'Hauptgericht', 'Shrimp Scampi', 820),
            ('sunsetgrill', 'Hauptgericht', 'BBQ Chicken Wrap', 750),
            ('sunsetgrill', 'Dessert', 'New York Cheesecake', 550),
            ('sunsetgrill', 'Dessert', 'Molten Chocolate Lava Cake', 600),
            ('sunsetgrill', 'Getränk', 'Mango Tango Smoothie', 350),
            ('sunsetgrill', 'Getränk', 'Pineapple Paradise', 400),
            ('sunsetgrill', 'Getränk', 'Berry Burst Lemonade', 300),
            ('sunsetgrill', 'Getränk', 'Iced Caramel Macchiato', 350),
                   
            ('fusiondelight', 'Vorspeise', 'Spring Rolls', 550),
            ('fusiondelight', 'Vorspeise', 'Potstickers', 600),
            ('fusiondelight', 'Vorspeise', 'Seaweed Salad', 500),
            ('fusiondelight', 'Vorspeise', 'Spicy Tuna Tartare', 650),
            ('fusiondelight', 'Hauptgericht', 'Sushi Burrito', 750),
            ('fusiondelight', 'Hauptgericht', 'Bibimbap', 800),
            ('fusiondelight', 'Hauptgericht', 'Pad Thai', 700),
            ('fusiondelight', 'Hauptgericht', 'General Tsos Tofu', 850),
            ('fusiondelight', 'Hauptgericht', 'Miso Glazed Salmon', 780),
            ('fusiondelight', 'Hauptgericht', 'Teriyaki Chicken Bowl', 820),
            ('fusiondelight', 'Hauptgericht', 'Vegetarian Ramen', 750),
            ('fusiondelight', 'Dessert', 'Matcha Green Tea Ice Cream', 550),
            ('fusiondelight', 'Dessert', 'Mango Sticky Rice', 600),
            ('fusiondelight', 'Getränk', 'Bubble Tea', 350),
            ('fusiondelight', 'Getränk', 'Lychee Mojito', 400),
            ('fusiondelight', 'Getränk', 'Passion Fruit Iced Tea', 300),
            ('fusiondelight', 'Getränk', 'Dragon Fruit Smoothie', 350),

            ('spicynoodlehouse', 'Vorspeise', 'Edamame', 550),
            ('spicynoodlehouse', 'Vorspeise', 'Spring Rolls', 600),
            ('spicynoodlehouse', 'Vorspeise', 'Kimchi', 500),
            ('spicynoodlehouse', 'Vorspeise', 'Prawn Tempura', 650),
            ('spicynoodlehouse', 'Hauptgericht', 'Spicy Ramen', 750),
            ('spicynoodlehouse', 'Hauptgericht', 'Dan Dan Noodles', 800),
            ('spicynoodlehouse', 'Hauptgericht', 'Szechuan Chicken', 700),
            ('spicynoodlehouse', 'Hauptgericht', 'Shrimp Pad Thai', 850),
            ('spicynoodlehouse', 'Hauptgericht', 'Beef Bulgogi Udon', 780),
            ('spicynoodlehouse', 'Hauptgericht', 'Vegetarian Pho', 820),
            ('spicynoodlehouse', 'Hauptgericht', 'Kimchi Fried Rice', 750),
            ('spicynoodlehouse', 'Dessert', 'Mango Sticky Rice', 550),
            ('spicynoodlehouse', 'Dessert', 'Green Tea Mochi', 600),
            ('spicynoodlehouse', 'Getränk', 'Thai Iced Tea', 350),
            ('spicynoodlehouse', 'Getränk', 'Lemon Ginger Soda', 400),
            ('spicynoodlehouse', 'Getränk', 'Cucumber Mint Cooler', 300),
            ('spicynoodlehouse', 'Getränk', 'Lychee Lemonade', 350),
                   
            ('greenoasiscafe', 'Vorspeise', 'Caprese Salad', 550),
            ('greenoasiscafe', 'Vorspeise', 'Quinoa Stuffed Mushrooms', 600),
            ('greenoasiscafe', 'Vorspeise', 'Hummus Plate', 500),
            ('greenoasiscafe', 'Vorspeise', 'Bruschetta', 650),
            ('greenoasiscafe', 'Hauptgericht', 'Vegan Buddha Bowl', 750),
            ('greenoasiscafe', 'Hauptgericht', 'Avocado and Chickpea Wrap', 800),
            ('greenoasiscafe', 'Hauptgericht', 'Mediterranean Quinoa Salad', 700),
            ('greenoasiscafe', 'Hauptgericht', 'Pesto Zoodle Bowl', 850),
            ('greenoasiscafe', 'Hauptgericht', 'Sweet Potato and Black Bean Tacos', 780),
            ('greenoasiscafe', 'Hauptgericht', 'Grilled Portobello Burger', 820),
            ('greenoasiscafe', 'Hauptgericht', 'Soba Noodle Stir-Fry', 750),
            ('greenoasiscafe', 'Dessert', 'Vegan Chocolate Cake', 550),
            ('greenoasiscafe', 'Dessert', 'Coconut Milk Ice Cream', 600),
            ('greenoasiscafe', 'Getränk', 'Kale Pineapple Smoothie', 350),
            ('greenoasiscafe', 'Getränk', 'Cucumber Mint Detox Water', 400),
            ('greenoasiscafe', 'Getränk', 'Turmeric Latte', 300),
            ('greenoasiscafe', 'Getränk', 'Berry Blast Smoothie', 350),

            ('stellarsteaks', 'Vorspeise', 'Garlic Bread', 550),
            ('stellarsteaks', 'Vorspeise', 'Shrimp Cocktail', 600),
            ('stellarsteaks', 'Vorspeise', 'Mushroom Bruschetta', 500),
            ('stellarsteaks', 'Vorspeise', 'Caesar Salad', 650),
            ('stellarsteaks', 'Hauptgericht', 'Filet Mignon', 750),
            ('stellarsteaks', 'Hauptgericht', 'Ribeye Steak', 800),
            ('stellarsteaks', 'Hauptgericht', 'Surf and Turf', 700),
            ('stellarsteaks', 'Hauptgericht', 'Lobster Tail', 850),
            ('stellarsteaks', 'Hauptgericht', 'Salmon Steak', 780),
            ('stellarsteaks', 'Hauptgericht', 'Chicken Marsala', 820),
            ('stellarsteaks', 'Hauptgericht', 'Vegetable Stir-Fry', 750),
            ('stellarsteaks', 'Dessert', 'New York Cheesecake', 550),
            ('stellarsteaks', 'Dessert', 'Chocolate Lava Cake', 600),
            ('stellarsteaks', 'Getränk', 'Red Wine', 350),
            ('stellarsteaks', 'Getränk', 'White Wine', 400),
            ('stellarsteaks', 'Getränk', 'Old Fashioned', 300),
            ('stellarsteaks', 'Getränk', 'Mint Julep', 350),

            ('thaiharmony', 'Vorspeise', 'Spring Rolls', 550),
            ('thaiharmony', 'Vorspeise', 'Tom Yum Soup', 600),
            ('thaiharmony', 'Vorspeise', 'Papaya Salad', 500),
            ('thaiharmony', 'Vorspeise', 'Chicken Satay', 650),
            ('thaiharmony', 'Hauptgericht', 'Pad Thai', 750),
            ('thaiharmony', 'Hauptgericht', 'Green Curry', 800),
            ('thaiharmony', 'Hauptgericht', 'Massaman Beef', 700),
            ('thaiharmony', 'Hauptgericht', 'Panang Chicken', 850),
            ('thaiharmony', 'Hauptgericht', 'Basil Chicken Stir-Fry', 780),
            ('thaiharmony', 'Hauptgericht', 'Pineapple Fried Rice', 820),
            ('thaiharmony', 'Hauptgericht', 'Duck Red Curry', 750),
            ('thaiharmony', 'Dessert', 'Mango Sticky Rice', 550),
            ('thaiharmony', 'Dessert', 'Coconut Ice Cream', 600),
            ('thaiharmony', 'Getränk', 'Thai Iced Tea', 350),
            ('thaiharmony', 'Getränk', 'Lychee Lemonade', 400),
            ('thaiharmony', 'Getränk', 'Tamarind Juice', 300),
            ('thaiharmony', 'Getränk', 'Cucumber Mint Cooler', 350),
                   
            ('cocoacraze', 'Vorspeise', 'Chocolate Covered Strawberries', 550),
            ('cocoacraze', 'Vorspeise', 'Chocolate Truffle Bruschetta', 600),
            ('cocoacraze', 'Vorspeise', 'Caprese Skewers with Balsamic Chocolate Glaze', 500),
            ('cocoacraze', 'Vorspeise', 'Chocolate Fondue with Fresh Fruit', 650),
            ('cocoacraze', 'Hauptgericht', 'Mole Chicken Enchiladas', 750),
            ('cocoacraze', 'Hauptgericht', 'Cocoa Rubbed BBQ Ribs', 800),
            ('cocoacraze', 'Hauptgericht', 'Chocolate Chili Con Carne', 700),
            ('cocoacraze', 'Hauptgericht', 'Cocoa Spiced Salmon', 850),
            ('cocoacraze', 'Hauptgericht', 'Chocolate Infused Penne Pasta', 780),
            ('cocoacraze', 'Hauptgericht', 'Cocoa Dusted Shrimp Scampi', 820),
            ('cocoacraze', 'Hauptgericht', 'Chocolate Risotto', 750),
            ('cocoacraze', 'Dessert', 'Dark Chocolate Mousse', 550),
            ('cocoacraze', 'Dessert', 'White Chocolate Raspberry Cheesecake', 600),
            ('cocoacraze', 'Getränk', 'Chocolate Martini', 350),
            ('cocoacraze', 'Getränk', 'Mint Chocolate Shake', 400),
            ('cocoacraze', 'Getränk', 'Chocolate Mint Iced Coffee', 300),
            ('cocoacraze', 'Getränk', 'Hazelnut Hot Chocolate', 350),

            ('mysticalmezze', 'Vorspeise', 'Hummus with Pita Bread', 550),
            ('mysticalmezze', 'Vorspeise', 'Baba Ganoush', 600),
            ('mysticalmezze', 'Vorspeise', 'Falafel', 500),
            ('mysticalmezze', 'Vorspeise', 'Stuffed Grape Leaves', 650),
            ('mysticalmezze', 'Hauptgericht', 'Shawarma Plate', 750),
            ('mysticalmezze', 'Hauptgericht', 'Moussaka', 800),
            ('mysticalmezze', 'Hauptgericht', 'Vegetarian Kebab', 700),
            ('mysticalmezze', 'Hauptgericht', 'Lentil Soup', 850),
            ('mysticalmezze', 'Hauptgericht', 'Greek Salad', 780),
            ('mysticalmezze', 'Hauptgericht', 'Chicken Souvlaki Wrap', 820),
            ('mysticalmezze', 'Hauptgericht', 'Spinach and Feta Pie', 750),
            ('mysticalmezze', 'Dessert', 'Baklava', 550),
            ('mysticalmezze', 'Dessert', 'Greek Yogurt with Honey and Walnuts', 600),
            ('mysticalmezze', 'Getränk', 'Ouzo', 350),
            ('mysticalmezze', 'Getränk', 'Tzatziki Smoothie', 400),
            ('mysticalmezze', 'Getränk', 'Mint Lemonade', 300),
            ('mysticalmezze', 'Getränk', 'Cucumber Greek Yogurt Drink', 350),

            ('saffronspice', 'Vorspeise', 'Safran-Suppe', 650),
            ('saffronspice', 'Vorspeise', 'Safran-Marinierte Garnelen', 700),
            ('saffronspice', 'Vorspeise', 'Gebratene Safran-Champignons', 600),
            ('saffronspice', 'Vorspeise', 'Safran-Honig-Glasierte Hähnchenflügel', 750),
            ('saffronspice', 'Hauptgericht', 'Safran-Hühnchen-Curry', 850),
            ('saffronspice', 'Hauptgericht', 'Safran-Gewürzreis mit Gemüse', 800),
            ('saffronspice', 'Hauptgericht', 'Lammragout mit Safransauce', 900),
            ('saffronspice', 'Hauptgericht', 'Safran-Zitronen-Hähnchen', 820),
            ('saffronspice', 'Hauptgericht', 'Safran-Fisch mit Kartoffeln', 780),
            ('saffronspice', 'Hauptgericht', 'Gemischte Pilaf mit Safran', 830),
            ('saffronspice', 'Dessert', 'Safran-Pistazien-Eis', 500),
            ('saffronspice', 'Dessert', 'Safran-Zuckerplätzchen', 550),
            ('saffronspice', 'Getränk', 'Safran-Rosmarin-Limonade', 350),
            ('saffronspice', 'Getränk', 'Safran-Minztee', 400),
            ('saffronspice', 'Getränk', 'Safran-Ingwer-Smoothie', 300),
            ('saffronspice', 'Getränk', 'Safran-Kardamom-Latte', 380),

            ('tropicaltaco', 'Vorspeise', 'Mango-Salsa mit Avocado', 650),
            ('tropicaltaco', 'Vorspeise', 'Ananas-Guacamole', 700),
            ('tropicaltaco', 'Vorspeise', 'Tropischer Meeresfrüchtesalat', 600),
            ('tropicaltaco', 'Vorspeise', 'Kokos-Limetten-Garnelen', 750),
            ('tropicaltaco', 'Hauptgericht', 'Tropischer Fisch-Taco', 850),
            ('tropicaltaco', 'Hauptgericht', 'Karibische Hähnchen-Enchiladas', 800),
            ('tropicaltaco', 'Hauptgericht', 'Guave-Glasierter Schweinebauch', 900),
            ('tropicaltaco', 'Hauptgericht', 'Mango-Chili-Hühnchen', 820),
            ('tropicaltaco', 'Hauptgericht', 'Tropischer Gemüseburrito', 780),
            ('tropicaltaco', 'Hauptgericht', 'Ananas-Rindfleisch-Tostadas', 830),
            ('tropicaltaco', 'Dessert', 'Kokos-Ananas-Sorbet', 500),
            ('tropicaltaco', 'Dessert', 'Passionsfrucht-Tiramisu', 550),
            ('tropicaltaco', 'Getränk', 'Guaven-Limetten-Margarita', 350),
            ('tropicaltaco', 'Getränk', 'Kokosnuss-Pina-Colada', 400),
            ('tropicaltaco', 'Getränk', 'Mango-Chili-Mojito', 300),
            ('tropicaltaco', 'Getränk', 'Tropischer Fruchtshake', 380),

            ('zwiebelzirkus', 'Vorspeise', 'Zwiebelringe mit Chili-Dip', 650),
            ('zwiebelzirkus', 'Vorspeise', 'Zwiebelsuppe mit Käsecroutons', 700),
            ('zwiebelzirkus', 'Vorspeise', 'Zwiebel-Balsamico-Bruschetta', 600),
            ('zwiebelzirkus', 'Vorspeise', 'Zwiebel-Kartoffel-Puffer', 750),
            ('zwiebelzirkus', 'Hauptgericht', 'Zwiebelrostbraten', 850),
            ('zwiebelzirkus', 'Hauptgericht', 'Gefüllte Zwiebeln mit Hackfleisch', 800),
            ('zwiebelzirkus', 'Hauptgericht', 'Zwiebel-Quiche', 900),
            ('zwiebelzirkus', 'Hauptgericht', 'Zwiebel-Honig-Hähnchen', 820),
            ('zwiebelzirkus', 'Hauptgericht', 'Zwiebel-Kartoffel-Gratin', 780),
            ('zwiebelzirkus', 'Hauptgericht', 'Zwiebel-Maultaschen', 830),
            ('zwiebelzirkus', 'Dessert', 'Zwiebel-Tarte Tatin', 500),
            ('zwiebelzirkus', 'Dessert', 'Zwiebel-Schokoladenkuchen', 550),
            ('zwiebelzirkus', 'Getränk', 'Zwiebel-Limonade', 350),
            ('zwiebelzirkus', 'Getränk', 'Zwiebel-Ingwer-Tee', 400),
            ('zwiebelzirkus', 'Getränk', 'Zwiebel-Minz-Smoothie', 300),
            ('zwiebelzirkus', 'Getränk', 'Zwiebel-Bier', 380),
                   
            ('wurstundsenf', 'Vorspeise', 'Weißwurst mit süßem Senf', 650),
            ('wurstundsenf', 'Vorspeise', 'Currywurst mit Pommes', 700),
            ('wurstundsenf', 'Vorspeise', 'Leberkäse-Semmel', 600),
            ('wurstundsenf', 'Vorspeise', 'Senf-Eingelegte Bratwurst', 750),
            ('wurstundsenf', 'Hauptgericht', 'Thüringer Rostbratwurst', 850),
            ('wurstundsenf', 'Hauptgericht', 'Debrecziner mit Sauerkraut', 800),
            ('wurstundsenf', 'Hauptgericht', 'Bockwurst mit Kartoffelsalat', 900),
            ('wurstundsenf', 'Hauptgericht', 'Weißwurst-Gulasch', 820),
            ('wurstundsenf', 'Hauptgericht', 'Nürnberger Rostbratwurst', 780),
            ('wurstundsenf', 'Hauptgericht', 'Senf-Sauerbraten', 830),
            ('wurstundsenf', 'Dessert', 'Senf-Eis mit Brezelstückchen', 500),
            ('wurstundsenf', 'Dessert', 'Senf-Honig-Pudding', 550),
            ('wurstundsenf', 'Getränk', 'Senf-Radler', 350),
            ('wurstundsenf', 'Getränk', 'Weißbier mit Senf', 400),
            ('wurstundsenf', 'Getränk', 'Senf-Limonade', 300),
            ('wurstundsenf', 'Getränk', 'Senf-Cocktail', 380),

            ('rheinweinhaus', 'Vorspeise', 'Käseplatte mit Trauben', 650),
            ('rheinweinhaus', 'Vorspeise', 'Rheinischer Sauerbraten-Salat', 700),
            ('rheinweinhaus', 'Vorspeise', 'Zwiebelkuchen mit Speck', 600),
            ('rheinweinhaus', 'Vorspeise', 'Obatzda mit Brezel', 750),
            ('rheinweinhaus', 'Hauptgericht', 'Rheinischer Sauerbraten mit Knödeln', 850),
            ('rheinweinhaus', 'Hauptgericht', 'Weinblatt-Gefüllte Forelle', 800),
            ('rheinweinhaus', 'Hauptgericht', 'Riesling-Hähnchen mit Spargel', 900),
            ('rheinweinhaus', 'Hauptgericht', 'Zanderfilet in Rieslingsoße', 820),
            ('rheinweinhaus', 'Hauptgericht', 'Schweinshaxe mit Sauerkraut', 780),
            ('rheinweinhaus', 'Hauptgericht', 'Rheinischer Zwiebelkuchen', 830),
            ('rheinweinhaus', 'Dessert', 'Rheinischer Apfelstrudel', 500),
            ('rheinweinhaus', 'Dessert', 'Trauben-Mascarpone-Dessert', 550),
            ('rheinweinhaus', 'Getränk', 'Rheinischer Riesling', 350),
            ('rheinweinhaus', 'Getränk', 'Gewürztraminer Spritzer', 400),
            ('rheinweinhaus', 'Getränk', 'Rheinischer Rotwein', 300),
            ('rheinweinhaus', 'Getränk', 'Rheinischer Winzersekt', 380),

            ('schwarzbrotstube', 'Vorspeise', 'Laugenbrezel mit Obatzda', 650),
            ('schwarzbrotstube', 'Vorspeise', 'Roggenbrot mit Leberwurst', 700),
            ('schwarzbrotstube', 'Vorspeise', 'Bauernbrot mit Griebenschmalz', 600),
            ('schwarzbrotstube', 'Vorspeise', 'Kartoffelsuppe mit Schwarzbrot-Croutons', 750),
            ('schwarzbrotstube', 'Hauptgericht', 'Sauerbraten mit Kartoffelknödeln', 850),
            ('schwarzbrotstube', 'Hauptgericht', 'Rinderrouladen mit Schwarzbrotfüllung', 800),
            ('schwarzbrotstube', 'Hauptgericht', 'Kartoffel-Gemüse-Auflauf mit Kräuterquark', 900),
            ('schwarzbrotstube', 'Hauptgericht', 'Kohlrouladen mit Schwarzbrotsoße', 820),
            ('schwarzbrotstube', 'Hauptgericht', 'Schweinebraten mit Schwarzbrotkruste', 780),
            ('schwarzbrotstube', 'Hauptgericht', 'Kartoffelsalat mit Schwarzbrotcroutons', 830),
            ('schwarzbrotstube', 'Dessert', 'Schwarzbrot-Eis mit Kirschsoße', 500),
            ('schwarzbrotstube', 'Dessert', 'Pumpernickel-Mousse', 550),
            ('schwarzbrotstube', 'Getränk', 'Schwarzbrot-Smoothie', 350),
            ('schwarzbrotstube', 'Getränk', 'Kümmel-Kwas', 400),
            ('schwarzbrotstube', 'Getränk', 'Schwarzbrot-Kaffee', 300),
            ('schwarzbrotstube', 'Getränk', 'Malzbier', 380),
            
            ('pilzparadies', 'Vorspeise', 'Champignon-Crostini', 550),
            ('pilzparadies', 'Vorspeise', 'Gebratene Pfifferlinge in Knoblauchbutter', 600),
            ('pilzparadies', 'Vorspeise', 'Pilz-Carpaccio mit Parmesan', 500),
            ('pilzparadies', 'Vorspeise', 'Gefüllte Shiitake-Pilze', 650),
            ('pilzparadies', 'Hauptgericht', 'Pilzrisotto mit Trüffelöl', 750),
            ('pilzparadies', 'Hauptgericht', 'Gefüllte Portobello-Pilze mit Spinat und Feta', 800),
            ('pilzparadies', 'Hauptgericht', 'Pilz-Gnocchi mit Salbei-Butter', 700),
            ('pilzparadies', 'Hauptgericht', 'Steinpilz-Ravioli mit Pilzrahmsauce', 850),
            ('pilzparadies', 'Hauptgericht', 'Pfifferlinge in Rahmsauce mit Semmelknödel', 780),
            ('pilzparadies', 'Dessert', 'Pilz-Tiramisu', 600),
            ('pilzparadies', 'Dessert', 'Pilz-Schokoladenmousse', 650),
            ('pilzparadies', 'Getränk', 'Pilz-Cocktail', 350),
            ('pilzparadies', 'Getränk', 'Pilz-Minz-Smoothie', 400),
            ('pilzparadies', 'Getränk', 'Pilz-Ingwer-Limonade', 300),
            ('pilzparadies', 'Getränk', 'Pilz-Latte', 350),
                   
            ('sauerkrautundwurst', 'Vorspeise', 'Sauerkrautbällchen mit Senf-Dip', 550),
            ('sauerkrautundwurst', 'Vorspeise', 'Wurstplatte mit verschiedenen Senfsorten', 600),
            ('sauerkrautundwurst', 'Vorspeise', 'Sauerkraut-Rouladen mit Hackfleisch', 500),
            ('sauerkrautundwurst', 'Vorspeise', 'Sauerkrautsuppe mit Mettwurst', 650),
            ('sauerkrautundwurst', 'Hauptgericht', 'Weisswurst mit Brezn und süßem Senf', 700),
            ('sauerkrautundwurst', 'Hauptgericht', 'Thüringer Rostbratwurst mit Sauerkraut', 800),
            ('sauerkrautundwurst', 'Hauptgericht', 'Hackbraten mit Sauerkraut und Kartoffelpüree', 750),
            ('sauerkrautundwurst', 'Hauptgericht', 'Wurstgulasch mit Sauerkrautnockerln', 850),
            ('sauerkrautundwurst', 'Hauptgericht', 'Kasseler mit Sauerkraut und Kartoffelsalat', 780),
            ('sauerkrautundwurst', 'Dessert', 'Sauerkrautstrudel mit Vanillesauce', 600),
            ('sauerkrautundwurst', 'Dessert', 'Senf-Eis mit Sauerkraut-Chips', 650),
            ('sauerkrautundwurst', 'Getränk', 'Sauerkraut-Smoothie', 350),
            ('sauerkrautundwurst', 'Getränk', 'Wurst-Wodka', 400),
            ('sauerkrautundwurst', 'Getränk', 'Senf-Mule', 300),
            ('sauerkrautundwurst', 'Getränk', 'Sauerkrautsaft', 350),
            
            ('cafebluerose', 'Vorspeise', 'Himbeer-Mandel-Cupcakes', 350),
            ('cafebluerose', 'Vorspeise', 'Vanille-Blumenkohl-Muffins', 300),
            ('cafebluerose', 'Vorspeise', 'Zitronen-Poppyseed-Scones', 400),
            ('cafebluerose', 'Vorspeise', 'Schokoladen-Chia-Pudding', 450),
            ('cafebluerose', 'Hauptgericht', 'Apfel-Zimt-Pfannkuchen', 550),
            ('cafebluerose', 'Hauptgericht', 'Blumenkohl-Walnuss-Waffeln', 500),
            ('cafebluerose', 'Hauptgericht', 'Himbeer-Mandel-French-Toast', 600),
            ('cafebluerose', 'Hauptgericht', 'Erdbeer-Bananen-Smoothie-Bowl', 650),
            ('cafebluerose', 'Dessert', 'Blue Rose Schokoladenkuchen', 700),
            ('cafebluerose', 'Dessert', 'Zitronen-Lavendel-Tarte', 750),
            ('cafebluerose', 'Getränk', 'Blumenkohl-Vanille-Latte', 400),
            ('cafebluerose', 'Getränk', 'Himbeer-Minz-Eistee', 350),
            ('cafebluerose', 'Getränk', 'Blue Rose Cappuccino', 450),
            ('cafebluerose', 'Getränk', 'Vanille-Rosenwasser-Limonade', 500);
        """)
    
    cursor.execute("""
        INSERT or REPLACE INTO Item (Restaurant, Name, IBeschreibung, Kategorie, Preis)
        VALUES ('mamamiapizza', 'Bruschetta', 'mit gehackten Tomaten und frischem Basilikum', 'Vorspeise', 550),
            ('mamamiapizza', 'Caprese-Salat', 'gesalzene rohe Tomatenscheiben mit Mozzarellascheiben, Basilikumblätter in Olivenöl beträufelt', 'Vorspeise', 650);
        """)
                    

    cursor.execute("""
        INSERT or REPLACE INTO Oeffnungszeit (GUsername, Wochentag, Von, Bis)
        VALUES ('cafebluerose', 'Montag', '00:00', '24:00'),
            ('cafebluerose', 'Mittwoch', '00:00', '24:00'),
            ('cafebluerose', 'Donnerstag', '00:00', '24:00'),
            ('cafebluerose', 'Freitag', '00:00', '24:00'),
            ('cafebluerose', 'Sonntag', '00:00', '24:00'),
                   
            ('sushiheaven', 'Dienstag', '00:00', '24:00'),
            ('sushiheaven', 'Mittwoch', '00:00', '24:00'),
            ('sushiheaven', 'Donnerstag', '00:00', '24:00'),
            ('sushiheaven', 'Freitag', '00:00', '24:00'),
            ('sushiheaven', 'Samstag', '00:00', '24:00'),
            ('sushiheaven', 'Sonntag', '00:00', '24:00'),
                   
            ('bowl', 'Montag', '00:00', '24:00'),
            ('bowl', 'Mittwoch', '00:00', '24:00'),
            ('bowl', 'Donnerstag', '00:00', '24:00'),
            ('bowl', 'Freitag', '00:00', '24:00'),
            ('bowl', 'Samstag', '00:00', '24:00'),
            ('bowl', 'Sonntag', '00:00', '24:00'),
                   
            ('americanstory', 'Montag', '00:00', '24:00'),
            ('americanstory', 'Dienstag', '00:00', '24:00'),
            ('americanstory', 'Donnerstag', '00:00', '24:00'),
            ('americanstory', 'Freitag', '00:00', '24:00'),
            ('americanstory', 'Samstag', '00:00', '24:00'),
                   
            ('sidebysoups', 'Montag', '00:00', '24:00'),
            ('sidebysoups', 'Mittwoch', '00:00', '24:00'),
            ('sidebysoups', 'Donnerstag', '00:00', '24:00'),
            ('sidebysoups', 'Samstag', '00:00', '24:00'),
            ('sidebysoups', 'Sonntag', '00:00', '24:00'),
            
            ('mamamiapizza', 'Montag', '00:00', '24:00'),
            ('mamamiapizza', 'Dienstag', '00:00', '24:00'),
            ('mamamiapizza', 'Donnerstag', '00:00', '24:00'),
            ('mamamiapizza', 'Freitag', '00:00', '24:00'),
            ('mamamiapizza', 'Samstag', '00:00', '24:00'),
            ('mamamiapizza', 'Sonntag', '00:00', '24:00'),
                   
            ('zoesgrill', 'Montag', '00:00', '24:00'),
            ('zoesgrill', 'Dienstag', '00:00', '24:00'),
            ('zoesgrill', 'Mittwoch', '00:00', '24:00'),
            ('zoesgrill', 'Donnerstag', '00:00', '24:00'),
            ('zoesgrill', 'Freitag', '00:00', '24:00'),
            ('zoesgrill', 'Samstag', '00:00', '24:00'),
            ('zoesgrill', 'Sonntag', '00:00', '24:00');
             
        """)
    
    
    
    dbcon.commit()