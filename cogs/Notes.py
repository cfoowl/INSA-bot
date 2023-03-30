from discord.ext import commands, tasks
import os
import json
import random
import datetime

def json_import(database):
        with open(database) as json_file:
            # Vérifie que le json n'est pas vide
            if os.stat(database).st_size == 0:
                notes = []
            else :
                notes = json.load(json_file)
        
        return notes

CHANNEL_ID = 1016652241211498556

class Notes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = "data/notes.json"
        self.channel = self.bot.get_channel(CHANNEL_ID)
        self.notes_check.start()

    @tasks.loop(minutes=10.0)
    async def notes_check(self):
        now = datetime.datetime.now()
        today8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
        today0am = now.replace(hour=0, minute=10, second=0, microsecond=0)

        if now > today8am or now < today0am:
            #import json
            notes_before = json_import(self.database)
            date_now = now.strftime("%d/%m/%Y %H:%M:%S")

            #run test.js
            os.system("node cogs/notes_scrapping.js")

            #import json
            notes_after = json_import(self.database)

            if len(notes_before) == len(notes_after):
                #formated date now
                
                print(f"{date_now}Pas de nouvelles notes !")
            elif len(notes_before) > len(notes_after):
                #rewrite json
                with open(self.database, 'w') as outfile:
                    json.dump(notes_before, outfile)
                print(f"{date_now}Une note a été supprimée !")
            else:
                #find new note
                for i in range(len(notes_after)):
                    if notes_after[i] not in notes_before:
                        await self.channel.send(f"@everyone Nouvelle note en {notes_after[i]}")
                    else:
                        notes_before.remove(notes_after[i])
        else :
            print("Pas l'heure de checker les notes !")