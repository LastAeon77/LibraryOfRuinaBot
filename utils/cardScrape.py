import aiohttp
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# import pandas as pd


async def get_site_content(currUrl):
    async with aiohttp.ClientSession() as session:
        async with session.get(currUrl) as resp:
            page = await resp.read()
    soup = BeautifulSoup(page, "lxml")
    return soup


async def get_site_request(currUrl):
    async with aiohttp.ClientSession() as session:
        async with session.get(currUrl) as resp:
            return await resp.read()


async def get_site_content_json(currUrl):
    async with aiohttp.ClientSession() as session:
        async with session.get(currUrl) as resp:
            page = await resp.json()
    return page


async def get_image_content(currUrl):
    async with aiohttp.ClientSession() as session:
        async with session.get(currUrl) as resp:
            page = await resp.read()
    return page


def make_into_string(df):
    Rarity = df[0][1][0]
    Rank = df[0][1][1]
    Guest = df[0][1][2]
    df[1] = df[1].fillna("-")
    OnPlayEff = df[1][1][0]
    Cost = df[1][1][1]
    df = df[2]
    df = df.fillna("-")
    RairtyAndStuff = f"""
    Rank: {Rank}
    Guest: {Guest}
    Rarity: {Rarity}
    OnPlayEff: {OnPlayEff}
    Cost: {Cost}
    """
    DmgRolls = df
    Dmg = f"""
    > {DmgRolls['Damage Rolls'][0]}
    > {DmgRolls['Damage Rolls'][1]}
    > {DmgRolls['Damage Rolls'][2]}
    > {DmgRolls['Damage Rolls'][3]}
    > {DmgRolls['Damage Rolls'][4]}
    """
    Types = f"""
    > {DmgRolls['Type'][0]}
    > {DmgRolls['Type'][1]}
    > {DmgRolls['Type'][2]}
    > {DmgRolls['Type'][3]}
    > {DmgRolls['Type'][4]}
    """
    Effects = f"""
    > {DmgRolls['Dice Effect'][0]}
    > {DmgRolls['Dice Effect'][1]}
    > {DmgRolls['Dice Effect'][2]}
    > {DmgRolls['Dice Effect'][3]}
    > {DmgRolls['Dice Effect'][4]}
    """

    return [RairtyAndStuff, Dmg, Types, Effects]


async def scrape_deck_image(listk):
    response = await get_image_content(listk[0])
    im1 = Image.open(BytesIO(response))
    response = await get_image_content(listk[1])
    im2 = Image.open(BytesIO(response))
    response = await get_image_content(listk[2])
    im3 = Image.open(BytesIO(response))
    response = await get_image_content(listk[3])
    im4 = Image.open(BytesIO(response))
    response = await get_image_content(listk[4])
    im5 = Image.open(BytesIO(response))
    response = await get_image_content(listk[5])
    im6 = Image.open(BytesIO(response))
    response = await get_image_content(listk[6])
    im7 = Image.open(BytesIO(response))
    response = await get_image_content(listk[7])
    im8 = Image.open(BytesIO(response))
    response = await get_image_content(listk[8])
    im9 = Image.open(BytesIO(response))

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
