# Description 
    
The Purpose of this Discord Bot is to ease the discussion of the game __Library of Ruina__. THis includes making decks, pulling out information etc etc


# Requirements:
    python version: 3.6+
    pip3 install pillow (PIL)
    pip3 install bs4
    pip3 install pandas
    pip3 install sqlite3
    import aiohttp
    import aiofiles

# Make json file for access token.

    Make resources/settings.json file and copy the folowing in:

    {
    "discord": {
        "owner": "",
        "token": "InsertTokenHere"
    }
    }
# Commands
    

## addCombatPage (Only availabe to ownter): Adds card to the csv file and also the image to the dtabase.   

    Example: ?addCombatPage Urban Shitpost,Thiccereth,10000,ShitPost,TRUE,2,Thiccereth Strike, https://cdn.discordapp.com/attachments/740565382586171402/746643340769886228/ThiccerethStrikes.png,,PaperBack,On Use: Destroys lolicons,1,Blunt,200-200,

## DeckMake:
    deck add: Create a new deck
        Example: ?deck add Oscar Pierce,High-speed Stabbing,High-speed Stabbing,High-speed Stabbing,High-speed Stabbing,High-speed Stabbing,High-speed Stabbing,High-speed Stabbing,High-speed Stabbing,High-speed Stabbing

    deck code: Searches for deck by code
        Example: ?deck code 2
    
    deck name: searches for deck by name
        Example: ?deck name Oscar Pierce
    
    deck mydeck: Displays all the deck you've made
        Example: ?deck mydeck

## Wiki(Still incomplete and in beta): Searches wiki and scrapes it's information
    Example: ?wiki Roland

## add: adds 2 integers
    Example: ?add 3 4
## search: Searches for a Card and will display it's stats
    Example: ?search to overcome crisis

## 2048 game: Play 2048, a legendary game!
    Example: ?tzfe
        to start
    Example: ?tzfe
        to quit
    
# Works Cited
    https://thispointer.com/python-how-to-append-a-new-row-to-an-existing-csv-file:~:text=Open%20our%20csv%20file%20in,in%20the%20associated%20csv%20file