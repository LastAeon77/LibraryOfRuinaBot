import pandas as pd


# When the name isn't available
# A class that can print out the possible names
class OtherOptions:
    def __init__(self, CardName):
        df = pd.read_csv("data/CardData.csv")
        self.df1 = df[df.Name.str[:1].str.lower() == CardName[:1].lower()]
        self.df2 = self.df1["Name"]

    def toString(self):
        final_str = ""
        for names in self.df2:
            final_str = final_str + "> " + names
            final_str = final_str + "\n"
        return final_str


# Newk=OtherOptions("the red notes")
# print(Newk.toString())
