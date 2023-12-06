import discord
from discord.ext import commands
import os

from help_cog import HelpCog
from music_cog import Music_Cog

bot = commands.Bot(command_prefix='/', intents=discord.Intents.default())

bot.remove_command('help')

bot.add_cog(HelpCog(bot))
bot.add_cog(Music_Cog(bot))

bot.run(os.getenv('TOKEN'))
