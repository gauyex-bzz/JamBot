import discord
from discord.ext import commands
import os

from help_cog import help_cog
from music_cog import music_cog

bot = commands.Bot(command_prefix='/')

bot.add_cog(help_cog(bot))
bot.add_cog(music_cog(bot))

bot.run(os.getenv('MTE1MTgwNzAwMjY1MDA4NzQzNQ.G8Wc6X._Al1K75CLn_hahI4rtG3jhZv2xPU0bKMQzwVVU'))
