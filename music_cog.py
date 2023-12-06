import discord
from discord.ext import commands

from youtube_dl import YoutubeDL


class Music_Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnected_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

        self.vc = None

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info('ytsearch:%s' % item, download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'[0]['url']], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())

        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            if self.vc is None:
                await ctx.send('Could not connect to the VC')
                return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())

        else:
            self.is_playing = False

    @commands.command(name='play', aliases=['p', 'playing'], help='Play the selected Song from YouTube')
    async def play(self, ctx, *args):
        query = ''.join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send('Connect to a voice channel to play something!')
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
        if type(song) is type(True):
            await ctx.send('Could not download the song. Incorrect format, try a different keyword')
        else:
            await ctx.send('Song added to queue')
            self.music_queue.append([song, voice_channel])

            if not self.is_playing:
                await self.play_music(ctx)

    @commands.command(name='pause', help='Pauses the current song')
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(name='resume', help='Resumes the current song')
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(name='skip', help='Skips the current song')
    async def skip(self, ctx, *args):
        if self.vc is not None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(name='queue', help='Displays all queued songs')
    async def queue(self, ctx):
        retval = ''

        for i in range(0, len(self.music_queue)):
            if i > 10:
                break
            retval += self.music_queue[i][0]['title'] + '\n'

        if retval != '':
            await ctx.send(retval)
        else:
            await ctx.send('Nothing to see here')
