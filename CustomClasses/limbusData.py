from discord.embeds import Embed
import discord
from discord.ui import Button, View
import json
import re
import os

BOT_SERVER_IMAGES = "http://138.197.42.244/"
PRIME_LINK = "https://malcute.aeonmoon.page"
EMOJI_LIMBUS_HEAD = "<:limbusheads:1280657716871692472>"
SIN_DICT = {
    "CRIMSON": "Wrath",
    "SCARLET": "Lust",
    "AMBER": "Sloth",
    "SHAMROCK": "Gluttony",
    "AZURE": "Gloom",
    "INDIGO": "Pride",
    "VIOLET": "Envy",
    "WHITE": "",
    "BLACK": "",
    "Crimson": "Wrath",
    "Scarlet": "Lust",
    "Amber": "Sloth",
    "Shamrock": "Gluttony",
    "Azure": "Gloom",
    "Indigo": "Pride",
    "Violet": "Envy",
    "White": "",
    "Black": "",
}

COLOR_DICT_SIN = {
    "CRIMSON": discord.Color.red(),
    "SCARLET": discord.Color.orange(),
    "AMBER": discord.Color.yellow(),
    "SHAMROCK": discord.Color.green(),
    "AZURE": discord.Color.blue(),
    "INDIGO": discord.Color.dark_blue(),
    "VIOLET": discord.Color.purple(),
    "WHITE": discord.Color.lighter_grey(),
    "BLACK": discord.Color.darker_grey(),
    "NEUTRAL": discord.Color.default() 
}
RESIST_NAMING = {
    0.5: "Ineffective",
    1: "Normal",
    2: "Fatal",
    0.75: "Endure",
    1.25: "Weak",
    0: "Immune",
}
ATTACK_TYPE_DICT = {
    "HIT": "Blunt",
    "Hit":"Blunt",
    "hit": "Blunt",
    "SLASH": "Slash",
    "Slash": "Slash",
    "slash": "Slash",
    "NONE": "",
    "PENETRATE": "Pierce",
    "Penetrate": "Pierce",
    "penetrate": "Pierce",
    "ATTACK": "",

}
color_dict = {
    1: discord.Color.green(),
    2: discord.Color.red(),
    3: discord.Color.gold(),
}


class DeleteButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Delete", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        view: EnemyView = self.view
        if interaction.user == view.author:
            try:
                await interaction.message.delete()
            except discord.Forbidden:
                await interaction.response.send_message(
                    "I cannot delete this message.", ephemeral=True
                )
            else:
                # Acknowledge the interaction so Discord doesn't show "This interaction failed"
                await interaction.response.defer()
        else:
            await interaction.response.send_message(
                "You cannot delete this message.", ephemeral=True
            )
            
with open("./data/Limbus_Data/EN_BattleKeywords.json", encoding="utf-8") as f:
    keyword_dict = json.load(f)["dataList"]

for file in os.listdir("./data/Limbus_Data"):
    if file.startswith("EN_BattleKeywords") and file.endswith(".json"):
        with open(f"./data/Limbus_Data/{file}", encoding="utf-8") as f:
            temp = json.load(f)["dataList"]
            keyword_dict.extend(temp)

BATTLEKEYWORD = {}
for dicts in keyword_dict:
    BATTLEKEYWORD["[" + dicts.get("id", "") + "]"] = dicts.get("name", "")
with open("./data/Limbus_Data/EN_SkillTag.json", encoding="utf-8") as f:
    keyword_dict = json.load(f)
keyword_dict = keyword_dict["dataList"]
for dicts in keyword_dict:
    BATTLEKEYWORD["[" + dicts.get("id", "") + "]"] = dicts.get("name", "")
def battle_keyword_dict():
    return BATTLEKEYWORD
def skill_description(skill_data: dict, skill_effect: dict, skill_num):
    def_type_dict = {
        "GUARD": "Guard",
        "EVADE": "Evade",
        "COUNTER": "Counter",
        "ATTACK": "",
    }
    ### Skill Data
    skill_id = skill_data.get("skill", "")
    atk_type = ATTACK_TYPE_DICT.get(skill_data["atk_type"], "NONE")
    def_type = def_type_dict.get(skill_data["def_type"], "ATTACK")
    attribute = skill_data.get("attribute_type", "")
    embed_color = COLOR_DICT_SIN.get(attribute, discord.Color.yellow())
    attribute = SIN_DICT.get(attribute)
    skill_target_type = skill_data.get("skill_target_type", "")
    weight = skill_data.get("target_num", "")
    sanityUse = skill_data.get("mp_usage", "")
    default_val = skill_data.get("default_value", "")
    if isinstance(skill_num, int) == False:
        skill_num = skill_num.get(skill_id)
    coin_roll_data = []
    icon_id = skill_data.get("icon_id", "")
    max_final = default_val
    for coins in skill_data.get("coin_roll", []):
        if coins.get("operator_type", "ADD") == "ADD":
            stuff = f" +{coins.get('scale','0')}"
            max_final += int(coins.get("scale", "0"))
        else:
            stuff = f" -{coins.get('scale','0')}"
            max_final -= int(coins.get("scale", "0"))
        coin_roll_data.append(stuff)
    coin_total = len(coin_roll_data)
    coin_total_str = EMOJI_LIMBUS_HEAD * coin_total
    coin_roll_data = ", ".join(coin_roll_data)
    ### Skill Effect
    name = skill_effect.get("name", "Unknown")
    onUse = skill_effect.get("desc", "")
    coin_desc = []
    keywords = "/".join(skill_effect.get("keywords", ["None"]))
    for coins in skill_effect["coin_descs"]:
        curr_index = coins.get("action_index")
        for desc in coins.get("descs", []):
            if desc != None:
                coin_desc.append(f"**{curr_index}**: " + desc)
    coin_desc = "\n".join(coin_desc)
    description = f"""
**Name**: {name}
 temporary_69420_str
**Damage/Defense Type**: {atk_type} {def_type}
**Attribute**: {attribute}
**Target Type**: {skill_target_type}
**Roll**: {default_val} / {coin_roll_data}
**Max Roll**: {max_final}
**Weight**: {weight}
**Sanity Used**: {sanityUse}
**Skill Num**: {skill_num}
**Key Word**: {keywords}
**Skill Effect**:
{onUse}
------ Coins ------
{coin_desc}
"""
    description = description.replace('<style="highlight">', "*").replace(
        "</style>", "*"
    )
    for word, en_name in BATTLEKEYWORD.items():
        description = description.replace(word, en_name)
    for word, en_name in SIN_DICT.items():
        description = description.replace(word, en_name)

    description = re.sub("<[^>]+>", "", description)
    description = description.replace("temporary_69420_str",coin_total_str)
    image_full_art_path = None
    if icon_id == "":
        image_full_art_path = (
            f"{BOT_SERVER_IMAGES}/limbus_images/Skill/Sprite/{skill_id}.png"
        )
    else:
        image_full_art_path = (
            f"{BOT_SERVER_IMAGES}/limbus_images/Skill/Sprite/{icon_id}.png"
        )
    return [name, description, image_full_art_path, embed_color]


class OneButton(discord.ui.Button):
    def __init__(self, name, description, image_path, color, image_file,private):
        super().__init__(style=discord.ButtonStyle.secondary, label=name)
        self.name = name[:32]
        self.description = description
        self.image_path = image_path
        self.color = color
        self.label = name
        self.image_file = image_file
        self.private = private

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        embed = Embed()
        embed.title = self.name
        embed.description = self.description
        embed.set_image(url=self.image_file)
        embed.color = self.color
        await interaction.response.defer(ephemeral=self.private)
        await interaction.edit_original_response(
            embed=embed,
            view=view,
        )


class ButtonEmbedView(discord.ui.View):
    def __init__(self, author, embeds_list,private = False, message=None):
        super().__init__()
        self.author = author
        self.message = message
        self.embeds_list = embeds_list  # [name,desc,image_file_path,color]
        self.private = private

        # Dynamically create and add buttons based on button_data
        for name, description, image_path, color in self.embeds_list:
            button = OneButton(
                name=name,
                description=description,
                image_path=image_path,
                color=color,
                image_file=image_path,
                private=self.private
            )
            self.add_item(button)

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.red)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.author:
            if self.private == False:
                await interaction.message.delete()


async def identity_data_analysis(
    interaction: discord.Interaction, data_in_json, uptie_level, max_level=45,private = False
):
    skill_effect = {}
    skill_data = {}
    passives = {}

    # get passive of greatest available uptie_level
    json_passives = data_in_json["passives"]
    json_passives_battle = sorted(
        [passive for passive in json_passives if not passive["is_support"]],
        key=lambda x: x["uptie_level"],
    )[::-1]
    json_passives_support = sorted(
        [passive for passive in json_passives if passive["is_support"]],
        key=lambda x: x["uptie_level"],
    )[::-1]
    battle_passive_max_uptie = -20

    for passi in json_passives_battle:
        if battle_passive_max_uptie == -20:
            if passi["uptie_level"] <= uptie_level:
                passives[passi["passive"]] = passi
                battle_passive_max_uptie = passi["uptie_level"]
        else:
            if passi["uptie_level"] == battle_passive_max_uptie:
                passives[passi["passive"]] = passi
    ############# Pasive Section ##################
    battle_passive_max_uptie = -20
    battle_passive_list = []
    for k, v in passives.items():
        name = v.get("ENDescription", {}).get("name", "")
        description = v.get("ENDescription", {}).get("desc", "")
        description = description.split("\n")
        for i in range(len(description)):
            if len(description[i]) > 0 and description[i][0] != "-":
                description[i] = "- " + description[i]
        description = "\n".join(description)
        attribution_list = []
        for attr in v.get("attribution", []):
            sin_type = attr.get("sinType", "")
            value = attr.get("value", -1)
            attr_type = attr.get("attribute_type", "")
            attribution_string = f"Sin: {sin_type} x{value} {attr_type}"
            attribution_list.append(attribution_string)
        attribution_list = "\n".join(attribution_list)
        final_pass_string = f"""*{name}*
{attribution_list}
{description}
"""
        battle_passive_list.append(final_pass_string)
    battle_passive_list = "\n".join(battle_passive_list)
    passives = {}
    for passi in json_passives_support:
        if battle_passive_max_uptie == -20:
            if passi["uptie_level"] <= uptie_level:
                passives[passi["passive"]] = passi
                battle_passive_max_uptie = passi["uptie_level"]
        else:
            if passi["uptie_level"] == battle_passive_max_uptie:
                passives[passi["passive"]] = passi
    support_passive_list = []
    for k, v in passives.items():
        name = v.get("ENDescription", {}).get("name", "")
        description = v.get("ENDescription", {}).get("desc", "")
        description = description.split("\n")
        for i in range(len(description)):
            if len(description[i]) > 0 and description[i][0] != "-":
                description[i] = "- " + description[i]
        description = "\n".join(description)
        attribution_list = []
        for attr in v.get("attribution", []):
            sin_type = attr.get("sinType", "")
            value = attr.get("value", -1)
            attr_type = attr.get("attribute_type", "")
            attribution_string = f"Sin: {sin_type} x{value} {attr_type}"
            attribution_list.append(attribution_string)
        attribution_list = "\n".join(attribution_list)
        final_pass_string = f"""*{name}*
{attribution_list}
{description}
"""
        support_passive_list.append(final_pass_string)
    support_passive_list = "\n".join(support_passive_list)

    ##################### Skill Data ###############
    for k, v in data_in_json["skill_data"].items():
        for dicts in v:
            if dicts["uptie_level"] == uptie_level:
                skill_data[k] = dicts

    for k, v in data_in_json["skill_effect"].items():
        for dicts in v:
            if dicts["uptie_level"] == uptie_level:
                skill_effect[k] = dicts
    hp = (
        data_in_json["HP"]["defaultStat"]
        + max_level * data_in_json["HP"]["incrementByLevel"]
    )
    minspeed = sorted(data_in_json["minSpeedList"])[uptie_level - 1]
    maxspeed = sorted(data_in_json["maxSpeedList"])[uptie_level - 1]
    uniqueAttribute = SIN_DICT.get(
        data_in_json["uniqueAttribute"], data_in_json["uniqueAttribute"]
    )
    breakSection = data_in_json["breakSection"]
    rarity = "0" * int(data_in_json["rarity"])
    defCorrection = data_in_json["defCorrection"]
    panicType = data_in_json["panicType"]
    sinner = data_in_json["characterId"]
    identity_id = data_in_json["id"]
    name = data_in_json["name"].replace("\n", " ")
    resist = []
    for i in data_in_json.get("attack_resist", []):
        temp_atk_type = ATTACK_TYPE_DICT[i.get("atk_type")]
        temp_atk_value = RESIST_NAMING.get(i.get("value"), "Unknown")
        temp = f"{temp_atk_type}: {temp_atk_value}({i.get('value')})"
        resist.append(temp)
    resist = ", ".join(resist)
    Identity_basic_description = f"""**Sinner**: {sinner}
**HP**: {int(hp)}
**Speed**: {minspeed}-{maxspeed}
**Attribute**: {uniqueAttribute}
**Weakness**: {resist}
**Stagger**: {','.join(map(str, breakSection))}
**Rarity**: {rarity}
**Panic**: {panicType}
**Passive**: 
{battle_passive_list}
**Support Passive**:
{support_passive_list}
"""
    Identity_basic_description = Identity_basic_description.replace(
        '<style="highlight">', "*"
    ).replace("</style>", "*")
    for word, en_name in BATTLEKEYWORD.items():
        Identity_basic_description = Identity_basic_description.replace(word, en_name)
    Identity_basic_description = re.sub("<[^>]+>", "", Identity_basic_description)
    for word, en_name in SIN_DICT.items():
        Identity_basic_description = Identity_basic_description.replace(word, en_name)

    image_full_art_path = None
    if uptie_level >= 3:
        image_full_art_path = f"{BOT_SERVER_IMAGES}/limbus_images/Identity/Sprite/{identity_id}_gacksung.png"
    else:
        image_full_art_path = (
            f"{BOT_SERVER_IMAGES}/limbus_images/Identity/Sprite/{identity_id}_normal.png"
        )

    descriptions = []
    descriptions.append(Identity_basic_description)
    embed = Embed()
    embed.title = f"{name}"
    embed.description = Identity_basic_description
    embed.color = color_dict.get(data_in_json["rarity"], discord.Color.green())
    embed.set_image(url=image_full_art_path)
    embed_list = [[name, Identity_basic_description, image_full_art_path, embed.color]]
    for keys in skill_data.keys():
        if keys not in skill_effect:
            continue  # or log an error or warning
        embed_list.append(
            skill_description(
                skill_data=skill_data[keys],
                skill_effect=skill_effect[keys],
                skill_num=data_in_json.get("skill_num", {}),
            )
        )

    buttons = ButtonEmbedView(interaction.user, embed_list,private=private)

    await interaction.response.send_message(
        embed=embed,
        view=buttons,
        ephemeral=private
    )


async def ego_data_analysis(
    interaction: discord.Interaction, data_in_json, uptie_level=4, private = False
):
    awakeningSkill = None
    corrosionSkill = None
    awakeningSkillEffect = None
    corrosionSkillEffect = None
    for i in data_in_json.get("awakeningSkill", []):
        if i.get("uptie_level") == uptie_level:
            awakeningSkill = i
            break
    for i in data_in_json.get("corrosionSkill", []):
        if i.get("uptie_level") == uptie_level:
            corrosionSkill = i
            break
    for i in data_in_json.get("awakeningSkillEffect", []):
        if i.get("uptie_level") == uptie_level:
            awakeningSkillEffect = i
            break
    awakeningSkillEffect["name"] = awakeningSkillEffect["name"] + " (Awakening)"
    for i in data_in_json.get("corrosionSkillEffect", []):
        if i.get("uptie_level") == uptie_level:
            corrosionSkillEffect = i
            break
    if corrosionSkillEffect:
        corrosionSkillEffect["name"] = corrosionSkillEffect["name"] + " (Corrision)"

    name = data_in_json.get("en_info", {}).get("name", "None")
    sinner = data_in_json.get("characterId", "")
    egoType = data_in_json.get("egoType", "")
    resist = []
    for i in data_in_json.get("attribute_resist", []):
        if i.get("type") != "WHITE" and i.get("type") != "BLACK":
            temp_type = SIN_DICT.get(i.get("type"))
            temp_atk_value = RESIST_NAMING.get(i.get("value"), "Unknown")
            temp = f"{temp_type}: {temp_atk_value}({i.get('value')})"
            resist.append(temp)
    resist = ", ".join(resist)
    requirement = []
    for i in data_in_json.get("requirement", []):
        temp_type = SIN_DICT.get(i.get("attributeType"))
        temp = f"{temp_type}({i.get('num')}) "
        requirement.append(temp)
    requirement = ", ".join(requirement)
    passives = []
    for i in data_in_json.get("passive", []):
        string = f"{i.get('name')}\n{i.get('desc')}"
        passives.append(string)
    passives = "\n".join(passives)
    description = f"""
**Name**: {name}
**Sinner**: {sinner}
**Ego Type**: {egoType}
**Requirement**: {requirement}
**Resistance**: {resist}
**Passives**:
{passives}
"""
    description = description.replace('<style="highlight">', "*").replace(
        "</style>", "*"
    )
    for word, en_name in BATTLEKEYWORD.items():
        description = description.replace(word, en_name)
    description = re.sub("<[^>]+>", "", description)
    for word, en_name in SIN_DICT.items():
        description = description.replace(word, en_name)

    ego_id = data_in_json["id"]
    embed = Embed()
    embed.title = f"{name}"
    image_full_art_path = (
        f"{BOT_SERVER_IMAGES}/limbus_images/Ego/Sprite/{ego_id}_cg.png"
    )
    embed.description = description
    embed.set_image(url=image_full_art_path)
    embed.color = discord.Color.green()
    embed_list = [[name, description, image_full_art_path, discord.Color.green()]]
    embed_list.append(
        skill_description(
            skill_data=awakeningSkill,
            skill_effect=awakeningSkillEffect,
            skill_num=1,
        )
    )
    if corrosionSkillEffect:
        embed_list.append(
            skill_description(
                skill_data=corrosionSkill,
                skill_effect=corrosionSkillEffect,
                skill_num=1,
            )
        )
    buttons = ButtonEmbedView(interaction.user, embed_list,private=private)
    await interaction.response.send_message(
        embed=embed,
        view=buttons,
        ephemeral=private
    )


def data_description_embed_generator(chapter_string,data,index):
    embed = Embed()
    embed.set_author(name=f"{chapter_string} - {str(index)}")
    teller = '???'  # Default to unknown speaker
    if data.get('teller',False):
        title = data.get('title', '???')
        teller_name = data.get('teller', '???')
        teller = f"{title} - {teller_name}".strip() if title else teller_name
    elif data.get('model',False):
        # Fallback to model information if no teller
        name = data['model'].get('enname', '')
        nickName = data['model'].get('enNickName', '')
        teller = f"{nickName} - {name}".strip() if nickName else name
    description = f"""
Place:{data.get('place','???')}
Dialouge #{data.get('id_raw','???')}
Speaker: {teller}
----------Content-----------
{data.get('content','-')}
"""
    embed.description = description
    return embed

class ButtonStoryEmbedView(discord.ui.View):
    def __init__(self, author, data_list, chapter_string,curr_index,private = False, message=None):
        super().__init__()
        self.author = author
        self.message = message
        self.chapter_string = chapter_string
        self.curr_index = curr_index
        self.data_list = data_list  # [name,desc,image_file_path,color]
        self.private = private
    @discord.ui.button(label="Delete", style=discord.ButtonStyle.red)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.author:
            if self.private == False:
                await interaction.message.delete()
    @discord.ui.button(label="-10", style=discord.ButtonStyle.red)
    async def minus_ten_story(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.author:
            self.curr_index = max(0,self.curr_index-10)
            embed = data_description_embed_generator(self.chapter_string,self.data_list[self.curr_index],self.curr_index)
            await interaction.response.defer()
            await interaction.message.edit(embed=embed)
    @discord.ui.button(label="-1", style=discord.ButtonStyle.red)
    async def minus_one_story(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.author:
            self.curr_index = max(0,self.curr_index-1)
            embed = data_description_embed_generator(self.chapter_string,self.data_list[self.curr_index],self.curr_index)
            await interaction.response.defer()
            await interaction.message.edit(embed=embed)    
    @discord.ui.button(label="+1", style=discord.ButtonStyle.red)
    async def plus_one_story(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.author:
            self.curr_index = min(len(self.data_list)-1,self.curr_index+1)
            embed = data_description_embed_generator(self.chapter_string,self.data_list[self.curr_index],self.curr_index)
            await interaction.response.defer()
            await interaction.message.edit(embed=embed)    
    @discord.ui.button(label="+10", style=discord.ButtonStyle.red)
    async def plus_ten_story(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.author:
            self.curr_index = min(len(self.data_list)-1,self.curr_index+10)
            embed = data_description_embed_generator(self.chapter_string,self.data_list[self.curr_index],self.curr_index)
            await interaction.response.defer()
            await interaction.message.edit(embed=embed)

async def story_data_display(
    interaction: discord.Interaction,chapter_string, data_in_json, index:int, private = False
):
    buttons = ButtonStoryEmbedView(author=interaction.user,data_list=data_in_json,curr_index=index, chapter_string=chapter_string)
    embed = data_description_embed_generator(chapter_string=chapter_string,data=data_in_json[index],index=index)
    await interaction.response.send_message(
        embed=embed,
        view=buttons,
        ephemeral=private
    )

###################### ENEMEY ##############################

def format_resists(resist_info: dict) -> str:
    atk_line = " | ".join([f"{r['type'].title()}: {r['value']}" for r in resist_info.get("atkResistList", [])])
    attr_line = " | ".join([f"{r['type'].title()}: {r['value']}" for r in resist_info.get("attributeResistList", [])])
    return f"**Atk Resist:** {atk_line}\n**Attr Resist:** {attr_line}"


# --- Singular Part Embed ---
def build_part_embed(enemy_id: str, part: dict, spoiler: bool = False):
    title = f"{part['EN_Name']}"
    if spoiler:
        title = f"||{title}||"

    embed = discord.Embed(
        title=title,
        color=discord.Color.green()
    )

    hp = part['hp']['defaultStat']
    resists = format_resists(part.get("resistInfo", {}))
    for word, en_name in BATTLEKEYWORD.items():
        resists = resists.replace(word, en_name)
    for word, en_name in SIN_DICT.items():
        resists = resists.replace(word, en_name)
    for word, en_name in ATTACK_TYPE_DICT.items():
        resists = resists.replace(word, en_name)

    stats_val = f"HP: {hp}\n{resists}"
    if spoiler:
        stats_val = f"||{stats_val}||"

    embed.add_field(
        name="Stats",
        value=stats_val,
        inline=False
    )
    return embed


# --- Singular Skill Embed ---
def build_skill_embed(enemy_id: str, skill: dict, spoiler: bool = False):
    data = skill["skillData"][0]
    effect = skill["skillEffect"]["levelList"][0]
    name = effect["name"]

    title = f"{name} (Tier {skill['skillTier']})"
    if spoiler:
        title = f"||{title}||"

    embed = discord.Embed(
        title=title,
        color=discord.Color.blue()
    )

    if "skillData" not in skill or "skillEffect" not in skill:
        desc = "No data available."
        if spoiler:
            desc = f"||{desc}||"
        embed.description = desc
        return embed

    desc = (
        f"Type: {data['atkType']}\n"
        f"Attr: {data['attributeType']}\n"
        f"Weight/Target Number: {data['targetNum']}\n"
        f"Base: {data['defaultValue']}\n\n"
        f"{effect.get('desc', '')}\n"
    )

    coins = data.get("coinList", [])
    coin_effects = effect.get("coinlist", [])
    for idx, coin in enumerate(coins):
        scale = coin['scale']
        effs = coin_effects[idx].get("coindescs", []) if idx < len(coin_effects) else []
        eff_text = " | ".join([e["desc"] for e in effs])
        desc += f"**{EMOJI_LIMBUS_HEAD} {idx+1}: +{scale}** → {eff_text}\n"

    for word, en_name in BATTLEKEYWORD.items():
        desc = desc.replace(word, en_name)
    for word, en_name in SIN_DICT.items():
        desc = desc.replace(word, en_name)
    if spoiler:
        desc = f"||{desc.strip()}||"

    embed.description = desc
    embed.color = COLOR_DICT_SIN[data['attributeType'].upper()]
    if not spoiler:
        embed.set_image(url=f"{BOT_SERVER_IMAGES}/limbus_images/Skill/Sprite/{skill['id']}.png")
    return embed


# --- Main Enemy Embed ---
def build_main_embed(enemy_id: str, enemy: dict, spoiler: bool = False):
    title = f"{enemy['EN_Name']} ({enemy_id})"
    if spoiler:
        title = f"||{title}||"

    embed = discord.Embed(
        title=title,
        color=discord.Color.purple()
    )

    desc = (
        f"**Risk Level**: {enemy['risk']}\n"
        f"**Level**: {enemy['level']}\n"
        f"**HP**: {enemy['hp']}\n\n"
    )
    passives = enemy.get("passives", [])
    for idx, passive in enumerate(passives, start=1):
        if passive is None:
            continue
        desc += f"**{idx}. {passive['name']}**\n{passive['desc']}\n\n"

    for word, en_name in BATTLEKEYWORD.items():
        desc = desc.replace(word, en_name)
    for word, en_name in SIN_DICT.items():
        desc = desc.replace(word, en_name)

    if spoiler:
        desc = f"||{desc.strip()}||"
    if not spoiler:
        embed.set_image(url=f"{BOT_SERVER_IMAGES}/limbus_images/portraits/Sprite/{enemy_id}_portrait.png")

    embed.description = desc
    file = None
    return embed, file


class MainButton(discord.ui.Button):
    def __init__(self, enemy_id: str, enemy: dict, spoiler=False):
        super().__init__(
            label="Main",
            style=discord.ButtonStyle.gray
        )
        self.enemy_id = enemy_id
        self.enemy = enemy
        self.spoiler = spoiler

    async def callback(self, interaction: discord.Interaction):
        view: EnemyView = self.view
        if interaction.user == view.author:
            embed, file = build_main_embed(self.enemy_id, self.enemy, self.spoiler)
            await interaction.response.edit_message(embed=embed, attachments=[file] if file else [], view=self.view)

# --- Interactive View ---
class EnemyView(discord.ui.View):
    def __init__(self, enemy_id: str, enemy_data: dict,spoiler = False):
        super().__init__(timeout=None)
        self.enemy_id = enemy_id
        self.enemy_data = enemy_data

        enemy = enemy_data[enemy_id]
        self.spoiler = spoiler

        self.add_item(MainButton(enemy_id, enemy_data[str(enemy_id)],self.spoiler))
        # Add one button per part
        for part in enemy["Parts"].values():
            self.add_item(PartButton(enemy_id, part, self.spoiler))

        # Add one button per skill
        for skill in enemy["Skills"].values():
            self.add_item(SkillButton(enemy_id, skill, self.spoiler))
        
        self.add_item(DeleteButton())

            

class PartButton(discord.ui.Button):
    def __init__(self, enemy_id, part_data: dict, spoiler = False):
        super().__init__(
            label=part_data["EN_Name"],
            style=discord.ButtonStyle.green
        )
        self.enemy_id = enemy_id
        self.part_data = part_data
        self.spoiler = spoiler


    async def callback(self, interaction: discord.Interaction):
        view: EnemyView = self.view
        if interaction.user == view.author:
            embed = build_part_embed(self.enemy_id, self.part_data, self.spoiler)
            await interaction.response.edit_message(embed=embed, view=self.view)


class SkillButton(discord.ui.Button):
    def __init__(self, enemy_id, skill_data: dict, spoiler = False):
        super().__init__(
            label=skill_data["skillEffect"]["levelList"][0]["name"],
            style=discord.ButtonStyle.blurple
        )
        self.enemy_id = enemy_id
        self.skill_data = skill_data
        self.spoiler = spoiler

    async def callback(self, interaction: discord.Interaction):
        view: EnemyView = self.view
        if interaction.user == view.author:
            embed = build_skill_embed(self.enemy_id, self.skill_data, self.spoiler)
            await interaction.response.edit_message(embed=embed, view=self.view)

