import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import unicodedata
import json

"""
TO DO
- owner only
- one role only"""

intents = discord.Intents.default()
intents.reactions = True
intents.members = True

client = commands.Bot(command_prefix = '!', intents = intents)


OWNER_ID = 269857981695393793

#Récupère la liste des messages d'attribution de rôle
with open('message_role.json') as json_file:
    #Vérifie que le json n'est pas vide
    if os.stat('message_role.json').st_size == 0:
        list_messages_reaction_role = []
    else :
        list_messages_reaction_role = json.load(json_file)

    #Duplique la liste d'id à écouter
    list_id_messages_reaction_role = []
    for i in range(len(list_messages_reaction_role)):
        list_id_messages_reaction_role.append(list_messages_reaction_role[i]["id"])
    print("Listes des messages à écouter : ")
    print(list_id_messages_reaction_role)

@client.event
async def on_ready():
    print('Bot is ready!')


@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id not in list_id_messages_reaction_role:
        return
    for i in list_messages_reaction_role:
        if payload.message_id == i["id"]:
            role_name = i.get(str(unicodedata.normalize('NFKD', payload.emoji.name).encode('ascii', 'ignore')))
            if role_name == None:
                return
            guild = client.get_guild(payload.guild_id)
            role = discord.utils.get(guild.roles, name=role_name)
            await payload.member.add_roles(role)
            break

@client.event
async def on_raw_reaction_remove(payload):
    if payload.message_id not in list_id_messages_reaction_role:
        return
    for i in list_messages_reaction_role:
        if payload.message_id == i["id"]:
            role_name = i.get(str(unicodedata.normalize('NFKD', payload.emoji.name).encode('ascii', 'ignore')))
            if role_name == None:
                return
            guild = client.get_guild(payload.guild_id)
            role = discord.utils.get(guild.roles, name=role_name)
            member = guild.get_member(payload.user_id)
            await member.remove_roles(role)
            break


@client.command()
async def role(ctx, *args):
        
    # Send the message
    message = await ctx.send('React with the following emojis to get the corresponding roles:')
    new_dict = {}
    new_dict |= {"id" : message.id}
    list_id_messages_reaction_role.append(message.id)
    

    # Add all the reactions to the message
    for i in range(0, len(args), 2):
        emoji = args[i]
        await message.add_reaction(emoji)
        role_name = args[i + 1]
        new_dict |= {str(unicodedata.normalize('NFKD', emoji).encode('ascii', 'ignore')):role_name}
    
    list_messages_reaction_role.append(new_dict)

    with open('message_role.json', 'w') as f:
        json.dump(list_messages_reaction_role, f)



#setup(bot)
load_dotenv(dotenv_path="config")
client.run(os.getenv("TOKEN"))