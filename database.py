import sqlite3

def executeUpdate(sql, params = ()):
    dbcon = sqlite3.connect("instance/db.db")
    cursor = dbcon.cursor()
    cursor.execute(sql, params)
    cursor.close()
    dbcon.commit()
    dbcon.close()

def getData(sql, params = ()):
    dbcon = sqlite3.connect("instance/db.db")
    cursor = dbcon.cursor()
    cursor.execute(sql, params)
    return cursor


def create_tables():
    dbcon = sqlite3.connect("instance/db.db")
    cursor = dbcon.cursor()
    
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS KundenAccount(
            Username varchar(50) PRIMARY KEY NOT NULL,
            Passwort varchar(100) NOT NULL,
            Nachname varchar(25) NOT NULL,
            Vorname varchar(25) NOT NULL,
            Strasse varchar(25) NOT NULL,
            Hausnummer int NOT NULL,
            Plz int NOT NULL
        )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS GeschaeftsAccount(
            Username varchar(50) PRIMARY KEY NOT NULL,
            Passwort varchar(100) NOT NULL,
            Strasse varchar(25) NOT NULL,
            Hausnummer int NOT NULL,
            Plz int NOT NULL
        )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Restaurant(
            Id int AUTO_INCREMENT NOT NULL,
            Name varchar(40),
            Beschreibung LONGTEXT,
            PRIMARY KEY(Id)
        )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Oeffnungszeit(
            Wochentag int,
            Von time,
            Bis time,
            PRIMARY KEY (Wochentag, Von, Bis)
        )""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Item(
            Id int AUTO_INCREMENT NOT NULL,
            Kategorie varchar(20),
            Name varchar(20),
            Preis int,
            PRIMARY KEY(Kategorie)
        )""")
    dbcon.commit()

def create_KundenAccount(username, passwort, nachname, vorname, strasse, hausnummer, plz):
    executeUpdate("""
        INSERT INTO KundenAccount (Username, Passwort, Nachname, Vorname, Strasse, Hausnummer, Plz)
            VALUES(?, ?, ?, ?, ?, ?, ?)""",
        (username, passwort, nachname, vorname, strasse, hausnummer, plz)
    )

def login_kunde(username, passwort):
    # Ergebnis des Vergleichs mit dem original pw aus db zum username
    request_pointer = getData("""SELECT Passwort FROM KundenAccount WHERE Username = ? """,(username,))
    
    result = request_pointer.fetchone()

    if result == None:
        return False
    
    origin_pw = result[0]
    
    return origin_pw == passwort