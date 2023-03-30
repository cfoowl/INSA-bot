import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from cogs.Role import Reaction_role
from cogs.Ping import Ping
from cogs.Notes import Notes
from cogs.help import HelpCog


# Initialisation
intents = discord.Intents.default()
intents.reactions = True
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix = '!', intents = intents)

@bot.event
async def on_ready():
    await setup(bot)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

async def setup(bot):
    bot.remove_command("help")
    await bot.add_cog(Reaction_role(bot,OWNER_ID))
    await bot.add_cog(Ping(bot))
    await bot.add_cog(Notes(bot))
    await bot.add_cog(HelpCog(bot))

# setup(bot)
load_dotenv(dotenv_path="data/config")
OWNER_ID = int(os.getenv("OWNER_ID"))
bot.run(os.getenv("TOKEN"))
