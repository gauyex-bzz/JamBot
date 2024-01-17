import discord
from discord.ext import commands
import os
from dotenv import load_dotenv


from help_cog import HelpCog
from music_cog import Music_Cog

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

bot.remove_command('help')

bot.add_cog(HelpCog(bot))
bot.add_cog(Music_Cog(bot))

load_dotenv()

bot.run(os.getenv('TOKEN'))
