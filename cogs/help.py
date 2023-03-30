import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
        title = "**INSA bot**",  
        description = "Préfixe : !",
        url= "https://github.com/AliceVancypher/INSA-bot",
        colour = 15277667)
        embed.add_field(name = "role", value = "créer un message à \"reaction-role\", faire !role --help pour plus d'infos", inline = False)
        await ctx.send(embed = embed)