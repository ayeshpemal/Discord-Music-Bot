import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
from collections import deque
import random

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Queue for songs and volume
song_queue = deque()
voice_client = None
default_volume = 0.5  # Default volume (50%)

# Suppress noise from yt-dlp and handle errors
youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': True,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '64',
    }],
}
ffmpeg_options = {
    'options': '-vn -b:a 64k'  # 64kbps bitrate
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=default_volume):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:  # Handle playlists or search results
            valid_entries = []
            skipped = 0
            for entry in data['entries']:
                if entry and 'url' in entry:
                    filename = entry['url'] if stream else ytdl.prepare_filename(entry)
                    valid_entries.append(cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=entry))
                else:
                    skipped += 1
            return valid_entries, skipped
        else:  # Single video
            if not data or 'url' not in data:
                raise Exception("Video is unavailable")
            filename = data['url'] if stream else ytdl.prepare_filename(data)
            return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data), 0

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Unified Play Command
@bot.command(name='play', help='Plays a song/playlist (URL or term) or selects from search (e.g., !play 1)')
async def play(ctx, *, arg=None):
    global voice_client
    if not ctx.author.voice:
        await ctx.send("You need to be in a voice channel to play music!")
        return

    channel = ctx.author.voice.channel
    if voice_client is None:
        voice_client = await channel.connect()
    elif voice_client.channel != channel:
        await voice_client.move_to(channel)

    # Check if arg is a number (for search results)
    if arg and arg.isdigit() and hasattr(ctx.bot, 'search_results'):
        index = int(arg)
        results = ctx.bot.search_results
        if 1 <= index <= len(results):
            player = results[index - 1]
            song_queue.append(player)
            await ctx.send(f'Added to queue: {player.title}')
            if not voice_client.is_playing():
                await play_next(ctx)
        else:
            await ctx.send("Invalid selection! Use a number from the search results.")
        return

    # Regular play with URL or search term
    if not arg:
        await ctx.send("Please provide a URL, search term, or number from search results!")
        return

    async with ctx.typing():
        try:
            result, skipped = await YTDLSource.from_url(arg, loop=bot.loop, stream=True)
            if isinstance(result, list):  # Playlist
                song_queue.extend(result)
                msg = f'Added playlist with {len(result)} songs to queue.'
                if skipped > 0:
                    msg += f' Skipped {skipped} unavailable video(s).'
                await ctx.send(msg)
            else:  # Single song
                song_queue.append(result)
                msg = f'Added to queue: {result.title}'
                if skipped > 0:
                    msg += f' (Skipped {skipped} unavailable video).'
                await ctx.send(msg)

            if not voice_client.is_playing():
                await play_next(ctx)
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

async def play_next(ctx):
    global voice_client
    if not song_queue:
        await ctx.send("Queue is empty!")
        return
    
    player = song_queue.popleft()
    voice_client.play(player, after=lambda e: bot.loop.create_task(play_next(ctx)))
    await ctx.send(f'Now playing: {player.title}')

# Command: Pause
@bot.command(name='pause', help='Pauses the current song')
async def pause(ctx):
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await ctx.send("Paused the music.")
    else:
        await ctx.send("Nothing is playing!")

# Command: Resume
@bot.command(name='resume', help='Resumes the paused song')
async def resume(ctx):
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await ctx.send("Resumed the music.")
    else:
        await ctx.send("Nothing is paused!")

# Command: Skip
@bot.command(name='skip', help='Skips the current song')
async def skip(ctx):
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Skipped the current song.")
    else:
        await ctx.send("Nothing is playing to skip!")

# Command: Stop
@bot.command(name='stop', help='Stops the music and clears the queue')
async def stop(ctx):
    global voice_client
    if voice_client:
        song_queue.clear()
        voice_client.stop()
        await voice_client.disconnect()
        voice_client = None
        await ctx.send("Stopped the music and left the channel.")
    else:
        await ctx.send("I'm not in a voice channel!")

# Command: Queue
@bot.command(name='queue', help='Shows the current queue')
async def queue(ctx):
    if not song_queue:
        await ctx.send("The queue is empty!")
    else:
        queue_list = "\n".join([f"{i+1}. {song.title}" for i, song in enumerate(song_queue)])
        await ctx.send(f"Current queue:\n{queue_list}")

# Command: Volume control
@bot.command(name='volume', help='Sets the volume (0-100)')
async def volume(ctx, vol: int):
    global voice_client
    if not voice_client or not voice_client.is_playing():
        await ctx.send("Nothing is playing!")
        return
    
    if 0 <= vol <= 100:
        new_volume = vol / 100
        voice_client.source.volume = new_volume
        await ctx.send(f"Volume set to {vol}%")
    else:
        await ctx.send("Volume must be between 0 and 100!")

# Command: Search for music by keyword with results
@bot.command(name='search', help='Searches YouTube and shows top 5 results')
async def search(ctx, *, keyword):
    async with ctx.typing():
        try:
            search_query = f"ytsearch5:{keyword}"
            results, skipped = await YTDLSource.from_url(search_query, loop=bot.loop, stream=True)
            if not results:
                await ctx.send("No results found!")
                return

            result_list = "\n".join([f"{i+1}. {result.title}" for i, result in enumerate(results)])
            await ctx.send(f"Search results for '{keyword}':\n{result_list}\nType `!play [number]` to play a song (e.g., `!play 1`).")
            ctx.bot.search_results = results  # Store results
        except Exception as e:
            await ctx.send(f"Error during search: {str(e)}")

# Command: Shuffle the queue
@bot.command(name='shuffle', help='Shuffles the current queue')
async def shuffle(ctx):
    if not song_queue:
        await ctx.send("The queue is empty!")
        return
    
    queue_list = list(song_queue)
    random.shuffle(queue_list)
    song_queue.clear()
    song_queue.extend(queue_list)
    await ctx.send("Queue has been shuffled!")

# Run the bot
bot.run('YOUR_ACTUAL_TOKEN')