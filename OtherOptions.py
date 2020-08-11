import pandas as pd
import os
from GuildAndToken import SEPORATOR

#When the name isn't available
class OtherOptions:
    def __init__(self, CardName):
        df = pd.read_csv("CardData.csv")
        self.df1 = df[df.Name.str[:1] == CardName[:1]]
        self.df2=self.df1['Name']
    def toString(self):
        final_str=''
        for names in self.df2:
            final_str=final_str+'> ' +names
            final_str=final_str+'\n'
        return final_str

Newk=OtherOptions("The red notes")
print(Newk.toString())