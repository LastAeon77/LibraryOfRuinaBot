import pandas as pd
import os
from GuildAndToken import SEPORATOR


class Card:
    def __init__(self, CardName):
        df = pd.read_csv("CardData.csv")
        df.fillna(0, inplace=True)
        df['Name'] = df['Name'].str.lower()
        row = df.loc[df['Name'] == CardName.lower()]
        self.id = (row.iloc[0]['Id'])
        self.chapter = (row.iloc[0]['Chapter'])
        self.obtainable = (row.iloc[0]['Obtainable'])
        self.cost = (row.iloc[0]['Cost'])
        self.name = (row.iloc[0]['Name'].capitalize())
        self.score = (row.iloc[0]['Score'])
        self.rarity = (row.iloc[0]['Rarity'])
        self.onPlay = (row.iloc[0]['On Play'])
        self.imageLink= (row.iloc[0]['Office']).replace("\\","/")
        temp = self.imageLink.split("/")
        self.imageName = temp[len(temp)-1]
        
        
        self.diceCount = (row.iloc[0]['DiceNumber'])
        self.diceDmg = []
        for i in range(int(self.diceCount)):
            self.diceDmg.append(
                str(i + 1) + ": " + (row.iloc[0]['D' + str(i + 1) + " Roll"]))
        self.diceDmgStr = SEPORATOR.join(self.diceDmg)
        self.diceType = []
        for i in range(int(self.diceCount)):
            self.diceType.append(
                str(i + 1) + ": " + (row.iloc[0]['D' + str(i + 1) + " Type"]))
        self.diceTypeStr = SEPORATOR.join(self.diceType)
        self.diceEff = []
        for i in range(int(self.diceCount)):
            if ((row.iloc[0]['D' + str(i + 1) + " Effect"]) != 0):
                self.diceEff.append(
                    str(i + 1) + ": " +
                    (row.iloc[0]['D' + str(i + 1) + " Effect"]))
            else:
                self.diceEff.append(str(i + 1) + ": ")
        self.diceEffStr = SEPORATOR.join(self.diceEff)

    def getID(self):
        return self.id

    def getChapter(self):
        return self.chapter

    def getObtainable(self):
        return self.obtainable

    def getCost(self):
        return self.cost

    def getName(self):
        return self.name

    def getScore(self):
        return self.score

    def getRarity(self):
        return self.rarity

    def getOnPlay(self):
        return self.onPlay

    def getDiceCount(self):
        return self.diceCount

    def getDiceDmg(self):
        return self.diceDmg

    def getDiceType(self):
        return self.diceType

    def getDiceEff(self):
        return self.diceEff

    def toString(self):
        final_str = (
            f"Name: {self.name}\n"
            f"Rarity: {self.rarity}\n"
            f"Chapter: {self.chapter}\n\n"
            f"**Stats**: \n"
            f"*Cost*: {self.cost}\n"
            f"*Dice Count*: {self.diceCount}\n"
            f"*On Play Effects*: {self.onPlay}\n"
            #f"*Die Type*:\n> {self.diceTypeStr}\n"
            #f"*Die Damage*:\n> {self.diceDmgStr}\n"
            #f"*Die Effect*:\n> {self.diceEffStr}\n"
        )
        return final_str


