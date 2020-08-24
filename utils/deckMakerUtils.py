import sqlite3
import pandas as pd
TABLENAME = "DeckLists"
DECK_SCHEMA = f"""
    CREATE TABLE IF NOT EXISTS {TABLENAME} (
        deck_code INTEGER,
        deck_name TEXT PRIMARY KEY,
        creator_name TEXT,
        card1 TEXT DEFAULT "Thiccereth Strike",
        card2 TEXT DEFAULT "Thiccereth Strike",
        card3 TEXT DEFAULT "Thiccereth Strike",
        card4 TEXT DEFAULT "Thiccereth Strike",
        card5 TEXT DEFAULT "Thiccereth Strike",
        card6 TEXT DEFAULT "Thiccereth Strike",
        card7 TEXT DEFAULT "Thiccereth Strike",
        card8 TEXT DEFAULT "Thiccereth Strike",
        card9 TEXT DEFAULT "Thiccereth Strike"
    );"""
DECK_INSERT = f"""
     INSERT INTO {TABLENAME} (deck_code,deck_name,creator_name,card1,card2,card3,card4,card5,card6,card7,card8,card9)
     VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
 """
DECKSPATH = "./data/decks.db"


def getPrevID():
    with sqlite3.connect(DECKSPATH) as c:
        cur = c.cursor()
        cur.execute(f"SELECT * FROM {TABLENAME}")
        data = cur.fetchall()
        return (data[-1][0])


def checkExist(listofcards):
    df = pd.read_csv("./data/CardData.csv")
    df.fillna(0, inplace=True)
    df["Name"] = df["Name"].str.lower()
    alteredList = listofcards[1:]
    for stuff in alteredList:
        row = df.loc[df["Name"] == stuff.lower()]
        if row.empty:
            return False
    return True
