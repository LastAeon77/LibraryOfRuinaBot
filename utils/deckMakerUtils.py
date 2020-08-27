import sqlite3
import pandas as pd
from PIL import Image

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
        return data[-1][0]


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


def returnImageLink(nameList):
    df = pd.read_csv("./data/CardData.csv")
    df["Name"] = df["Name"].str.lower()
    newlist = []
    df = df.fillna(0, inplace=True)
    for names in nameList:
        row = df.loc[df["Name"] == names.lower()]
        if row.iloc[0]["Office"] != 0:
            newlist.append(row.iloc[0]["Office"])
        else:
            newlist.append("Card/NotAvailable.PNG")
    return newlist


def deckImgMaker(listk):
    # print(listk)

    im1 = Image.open(listk[0].replace("\\", "/")).resize((410, 310))
    im2 = Image.open(listk[1].replace("\\", "/")).resize((410, 310))
    im3 = Image.open(listk[2].replace("\\", "/")).resize((410, 310))
    im4 = Image.open(listk[3].replace("\\", "/")).resize((410, 310))
    im5 = Image.open(listk[4].replace("\\", "/")).resize((410, 310))
    im6 = Image.open(listk[5].replace("\\", "/")).resize((410, 310))
    im7 = Image.open(listk[6].replace("\\", "/")).resize((410, 310))
    im8 = Image.open(listk[7].replace("\\", "/")).resize((410, 310))
    im9 = Image.open(listk[8].replace("\\", "/")).resize((410, 310))
    (width1, height1) = im1.size
    result_width = width1 * 3
    result_height = height1 * 3
    imFinal = Image.new("RGB", (result_width, result_height))
    imFinal.paste(im=im1, box=(0, 0))
    imFinal.paste(im=im2, box=(width1, 0))
    imFinal.paste(im=im3, box=(width1 * 2, 0))
    imFinal.paste(im=im4, box=(0, height1))
    imFinal.paste(im=im5, box=(width1, height1))
    imFinal.paste(im=im6, box=(width1 * 2, height1))
    imFinal.paste(im=im7, box=(0, height1 * 2))
    imFinal.paste(im=im8, box=(width1, height1 * 2))
    imFinal.paste(im=im9, box=(width1 * 2, height1 * 2))
    return imFinal
