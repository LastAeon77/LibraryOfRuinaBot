# from bs4 import BeautifulSoup
# import requests
# import discord
# from discord.ext import commands
# import pandas as pd


# class LibraryScrape:
#     def __init__(self, searchTerm):
#         df = pd.read_csv("./data/wiki.csv")
#         row = df.loc[df["SearchTerms"].str.lower() == searchTerm.lower()]
#         self.searchType = row.iloc[0]["Type"]
#         self.link = "https://library-of-ruina.fandom.com/wiki/" + searchTerm
#         source = requests.get(self.link).text
#         self.soup = BeautifulSoup(source, "lxml")
#         self.imageLink = ""
#         self.contents = ""

#     def Characters(self):
#         img = self.soup.find_all("figure", attrs={"class": "pi-item pi-image"})
#         k = []
#         for imgs in img:
#             k.append(imgs.find("img"))
#         src = k[0].attrs["src"]
#         self.imageLink = src
#         words = self.soup.find_all("p")
#         temp = []
#         for paragraphs in words:
#             temp.append(paragraphs)
#         self.contents += temp[1].get_text()
#         self.contents += "\n"
#         self.contents += temp[2].get_text()
#         self.contents += "\n"
#         self.contents += self.link

#         final = []
#         final.append(self.imageLink)
#         final.append(self.contents)
#         return final

#     def Mechanics(self):
#         img = self.soup.find_all(
#             "figure", attrs={"class": "article-thumb tright show-info-icon"}
#         )

#         k = []
#         for imgs in img:
#             k.append(imgs.find("img"))
#         src = k[0].attrs["src"]
#         self.imageLink = src
#         words = self.soup.find_all("p")
#         temp = []
#         for paragraphs in words:
#             temp.append(paragraphs)
#         self.contents += temp[1].get_text()
#         self.contents += "\n"
#         self.contents += temp[2].get_text()
#         # self.contents += temp[3].get_text()
#         final = []
#         final.append(self.imageLink)
#         final.append(self.contents)
#         return final

#     def Floors(self):
#         try:
#             img = self.soup.find_all("a", attrs={"class": "image image-thumbnail"})
#             k = []
#             for imgs in img:
#                 k.append(imgs)
#             src = k[0]["href"]
#             self.imageLink = src
#         except:
#             self.imageLink = "https://i.imgflip.com/j69nf.jpg"
#         words = self.soup.find_all("p")
#         temp = []
#         for paragraphs in words:
#             temp.append(paragraphs)
#         self.contents += temp[1].get_text()
#         self.contents += "\n"
#         self.contents += temp[2].get_text()
#         final = []
#         final.append(self.imageLink)
#         final.append(self.contents)
#         return final


# class LibraryStuff(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot

#     @commands.command()
#     async def wiki(self, ctx, arx: str):
#         """Searches wiki for topics"""
#         name = arx
#         embed = discord.Embed()
#         embed.color = 3066993
#         embed.set_author(name=str(arx))
#         link = ""
#         content = ""
#         try:
#             temp = LibraryScrape(name)

#             if temp.searchType == "Characters":
#                 link, content = temp.Characters()
#             elif temp.searchType == "Floors":
#                 link, content = temp.Floors()
#             elif temp.searchType == "Mechanics":
#                 link, content = temp.Mechanics()
#         except:
#             link = "https://i.imgflip.com/j69nf.jpg"
#             content = "Content not found, either it doesn't"
#             content += " exist or Master Last_Aeon was lazy"
#             content += "\n If you typed floor, try Floor_of_History"
#         embed.set_image(url=link)
#         embed.set_author(name=name.capitalize())
#         embed.description = content
#         await ctx.send(embed=embed)


# def setup(bot):
#     bot.add_cog(LibraryStuff(bot))


# x = LibraryScrape("key_pages")
# print(x.Mechanics())
# link = "https://library-of-ruina.fandom.com/wiki/Floor_of_History"
# source = requests.get(link).text
# soup = BeautifulSoup(source, "lxml")
# img = soup.find_all("a", attrs={"class": "image image-thumbnail"})

# k = []
# for imgs in img:
#     k.append(imgs)

# print(k[0]["href"])

# x = LibraryScrape("Invitations")
# print(x.Mechanics())

# img = soup.find('div', class_=' image-WikiaSiteWrapper')
# #find all stff with figure and class name this
# summary = soup.find_all("figure", attrs={"class":"pi-item pi-image"})
# #print(summary)
# k=[]
# #find image
# for imgs in summary:
#     k.append(imgs.find("img"))
# #summary = img.find('div', class_='image-WikiaSiteWrapper')

# #print(k[0].attrs)
# #get the image src from attributes
# src = k[0].attrs['src']
# #print(src)
# #get link
# img_link=src
# img = requests.get(img_link)
# #download
# #with open("cogs/angela.png", "wb") as f:
#     #f.write(img.content)


# words = soup.find_all("p")
# temp=[]
# for paragraphs in words:
#     temp.append(paragraphs)

# temp[0]


# print(temp[2].get_text())
