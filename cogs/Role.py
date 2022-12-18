import discord
from discord.ext import commands
import os
import unicodedata
import json

class Reaction_role(commands.Cog):
    def __init__(self, bot, owner_id):
        self.bot = bot
        self.database = 'data/message_role.json'
        self.list_messages = self.list_messages_import()
        self.list_id = self.list_id_init()
        self.owner_id = owner_id
        

    

    # Récupère la liste des messages d'attribution de rôle
    def list_messages_import(self):
        with open(self.database) as json_file:
            # Vérifie que le json n'est pas vide
            if os.stat(self.database).st_size == 0:
                list_messages_reaction_role = []
            else :
                list_messages_reaction_role = json.load(json_file)
        
        return list_messages_reaction_role
    
    # Duplique la liste d'id à écouter
    def list_id_init(self):
        list_id_messages_reaction_role = []
        for i in range(len(self.list_messages)):
            list_id_messages_reaction_role.append(self.list_messages[i]["id"])
        return list_id_messages_reaction_role
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """
        Ecoute les réactions arrivant sur les messages présents dans la liste
        Ajoute le rôle correspondant à la reaction ajoutée par l'utilisateur
        """

        # ID du message présent ou non dans la liste
        if payload.message_id not in self.list_id:
            return

        # Récupère le dictionnaire qui correspond au message
        for i in self.list_messages:
            if payload.message_id == i["id"]:

                # Si UF = 1, alors on vérifie que l'utilisateur n'a pas déjà un des rôles de la liste
                if i["UF"] == 1:
                    for v in i.values():
                        if discord.utils.get(payload.member.roles, name=v) != None:
                            print(f"{payload.member} already has the role {v}")
                            return
                
                # Récupère le nom du rôle correspond à la réaction
                role_name = i.get(str(unicodedata.normalize('NFKD', payload.emoji.name).encode('ascii', 'ignore')))
                if role_name == None:
                    return
                
                # Récupère le rôle sur le serveur
                guild = self.bot.get_guild(payload.guild_id)
                role = discord.utils.get(guild.roles, name=role_name)

                # Ajoute le rôle à l'utilisateur
                await payload.member.add_roles(role)
                break
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """
        Ecoute les réactions arrivant sur les messages présents dans la liste
        Enlève le rôle correspondant à la reaction enlevée par l'utilisateur
        """
        
        # ID du message présent ou non dans la liste
        if payload.message_id not in self.list_id:
            return

        # Récupère le dictionnaire qui correspond au message
        for i in self.list_messages:
            if payload.message_id == i["id"]:
                
                # Si le Remove Flag = 0, alors on n'enlève pas le rôle
                if i["RF"] == 0:
                    return

                # Récupère le nom du rôle correspond à la réaction
                role_name = i.get(str(unicodedata.normalize('NFKD', payload.emoji.name).encode('ascii', 'ignore')))
                if role_name == None:
                    return
                
                # Récupère le rôle et l'utilisateur sur le serveur
                guild = self.bot.get_guild(payload.guild_id)
                role = discord.utils.get(guild.roles, name=role_name)
                member = guild.get_member(payload.user_id)

                # Enlève le rôle à l'utilisateur
                await member.remove_roles(role)
                break
    
    @commands.command()
    async def role(self, ctx, *args):
    
        help_str = f"""
    __**ROLE**__

    ⚠️Cette commande n'est utilisable que par {self.bot.get_user(self.owner_id)} ⚠️

    !Role permet de générer un message de reaction role (les membres peuvent s'auto ajouter/enlever des rôles avec les réactions sous le message).
    Peut avoir 1 à n (limite maximale inconnue pour le moment) paire réaction-role comme argument.

    **UTILISATION**
        `!role <option1> <option2> ... <emote1> <role1> <emote2> <role2> ...`

    **OPTIONS**
        `-h  | --help` : manuel
        `-m  | --message 'str'` : Personnalise le message envoyé par le bot. Le message doit être entouré de quote < ' >
        `-nr | --no-remove` : Les membres ne peuvent pas s'enlever le rôle en enlevant la réaction
        `-u  | --unique` : Les membres peuvent avoir uniquement 1 rôle de la liste
        """
        # Check des permissions
        if ctx.message.author.id != self.owner_id:
            await ctx.send(help_str)
            return
        
        if len(args) == 0:
            await ctx.send(help_str)
            return

        # Default values
        message_str = "Réagissez avec le(s) emoji(s) suivant(s) pour avoir le(s) rôle(s) correspondant : "  # Default message
        UF = 0                                                                                              # Unique Flag
        RF = 1                                                                                              # Remove Flag

        start = 0

        # OPTIONS
        while args[start].startswith("-"):
            match args[start]:
                # HELP
                case "-h" |"--help":
                    await ctx.send(help_str)
                    return

                # MESSAGE
                case "-m" | "--message":
                    try :
                        if args[start+1].startswith('"') or args[start+1].startswith("'"):
                            start += 1
                            message_str = args[start]
                            if not(args[start].endswith('"') or args[start].endswith("'")):
                                while(not(args[start].endswith('"') or args[start].endswith("'"))):
                                    message_str = message_str + " " + args[start+1]
                                    start += 1
                            message_str = message_str[1:-1]
                            message_str = message_str[:2000]
                        else :
                            await ctx.send("ERREUR : il manque sûrement un début de quote ( ' ) pour l'option -m")
                            return
                    except IndexError: await ctx.send("ERREUR : il manque sûrement une fin de quote ( ' ) pour l'option -m")
                
                # NO-REMOVE
                case "-nr" | "--no-remove":
                    RF = 0

                # UNIQUE
                case "-u" | "--unique": 
                    UF = 1
                    
                case _ : print("Unknown")
            start += 1

        # Envoie le message
        message = await ctx.send(message_str)

        # Stock l'id du message envoyé 
        new_dict = {}
        new_dict |= {"id" : message.id}

        # Stock les différents flags
        new_dict |= {"UF" : UF}
        new_dict |= {"RF" : RF}
        

        # Ajoute chaque paire réaction-rôle
        for i in range(start, len(args), 2):
            emoji = args[i]

            # Ajout de la réaction
            try : 
                await message.add_reaction(emoji)
            except Exception : 
                await ctx.send(f"""ERREUR : "{emoji}" n'est pas un emoji existant""")
                await message.delete()
                return
            
            # Ajout du rôle
            try : role_name = args[i + 1]
            except IndexError:
                await ctx.send(f"""ERREUR : Missing one last argument""")
                await message.delete()
                return

            if discord.utils.get(ctx.guild.roles, name=role_name) == None:
                await ctx.send(f"""ERREUR : "{role_name}" n'existe pas""")
                await message.delete()
                return

            # Ajout de la paire dans le dictionnaire 
            new_dict |= {str(unicodedata.normalize('NFKD', emoji).encode('ascii', 'ignore')):role_name}
        
        # Mise à jour du json
        self.list_id.append(message.id)
        self.list_messages.append(new_dict)
        with open(self.database, 'w') as f:
            json.dump(self.list_messages, f)

            