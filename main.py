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

# Récupère la liste des messages d'attribution de rôle
with open('message_role.json') as json_file:
    # Vérifie que le json n'est pas vide
    if os.stat('message_role.json').st_size == 0:
        list_messages_reaction_role = []
    else :
        list_messages_reaction_role = json.load(json_file)

    # Duplique la liste d'id à écouter
    list_id_messages_reaction_role = []
    for i in range(len(list_messages_reaction_role)):
        list_id_messages_reaction_role.append(list_messages_reaction_role[i]["id"])

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_raw_reaction_add(payload):
    """
    Ecoute les réactions arrivant sur les messages présents dans la liste
    Ajoute le rôle correspondant à la reaction ajoutée par l'utilisateur
    """

    # ID du message présent ou non dans la liste
    if payload.message_id not in list_id_messages_reaction_role:
        return

    # Récupère le dictionnaire qui correspond au message
    for i in list_messages_reaction_role:
        if payload.message_id == i["id"]:
            # Récupère le nom du rôle correspond à la réaction
            role_name = i.get(str(unicodedata.normalize('NFKD', payload.emoji.name).encode('ascii', 'ignore')))
            if role_name == None:
                return
            
            # Récupère le rôle sur le serveur
            guild = client.get_guild(payload.guild_id)
            role = discord.utils.get(guild.roles, name=role_name)

            # Ajoute le rôle à l'utilisateur
            await payload.member.add_roles(role)
            break

@client.event
async def on_raw_reaction_remove(payload):
    """
    Ecoute les réactions arrivant sur les messages présents dans la liste
    Enlève le rôle correspondant à la reaction enlevée par l'utilisateur
    """

    # ID du message présent ou non dans la liste
    if payload.message_id not in list_id_messages_reaction_role:
        return

    # Récupère le dictionnaire qui correspond au message
    for i in list_messages_reaction_role:
        if payload.message_id == i["id"]:
            # Récupère le nom du rôle correspond à la réaction
            role_name = i.get(str(unicodedata.normalize('NFKD', payload.emoji.name).encode('ascii', 'ignore')))
            if role_name == None:
                return
            
            # Récupère le rôle et l'utilisateur sur le serveur
            guild = client.get_guild(payload.guild_id)
            role = discord.utils.get(guild.roles, name=role_name)
            member = guild.get_member(payload.user_id)

            # Enlève le rôle à l'utilisateur
            await member.remove_roles(role)
            break


@client.command()
async def role(ctx, *args):
        
    # Envoie le message
    message = await ctx.send('Réagissez avec le(s) emoji(s) suivant(s) pour avoir le(s) rôle(s) correspondant : ')

    # Stock l'id du message envoyé 
    new_dict = {}
    new_dict |= {"id" : message.id}
    list_id_messages_reaction_role.append(message.id)
    

    # Ajoute chaque paire emoji-rôle
    for i in range(0, len(args), 2):
        emoji = args[i]
        await message.add_reaction(emoji)
        role_name = args[i + 1]
        new_dict |= {str(unicodedata.normalize('NFKD', emoji).encode('ascii', 'ignore')):role_name}
    
    # Mise à jour du json
    list_messages_reaction_role.append(new_dict)
    with open('message_role.json', 'w') as f:
        json.dump(list_messages_reaction_role, f)



# setup(bot)
load_dotenv(dotenv_path="config")
client.run(os.getenv("TOKEN"))