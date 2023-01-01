import discord
import asyncio
from discord.ext import commands, tasks
import os
import random
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL
import sys
import spotipy
import spotipy.util as util
import youtube_dl

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=".", intents=intents)

# Set the intents for the bot
intents.members = True
intents.presences = True
intents.typing = True
intents.message_content = True

client2 = discord.Client(intents=intents)

client = commands.Bot(command_prefix='.', intents=intents)

async def customresponse():
    # Wait for 5 seconds before checking for new messages
    await asyncio.sleep(5)
    # Check for new messages
    await client2.wait_until_ready()
    while not client2.is_closed():
        async for message in client2.get_channel(642467912791097356).history(limit=1):
            # Ignore messages from the bot itself
            if message.author == client2.user:
                continue
            if message.content == "MESSAGE":
                # The bot will reply with a message when someone says "chi?"
                await message.channel.send("REPLY")
        # Wait for 5 seconds before checking for new messages again
        await asyncio.sleep(5)

@client.event
async def on_ready():
    # Create the task when the bot is ready
    client.loop.create_task(customresponse())


########################################################################################################################

audio_data = None

CLIENT_ID = "your spotify api client id"
CLIENT_SECRET = "your spotify api client secret"
REDIRECT_URI = "http://localhost:8888/callback"
USERNAME = "your-username"
scope = "user-read-private user-read-playback-state user-modify-playback-state"
token = util.prompt_for_user_token(USERNAME, scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
spotify_api = spotipy.Spotify(auth=token)

players = {}

@client.event  # check if bot is ready
async def on_ready():
    print('Bot online')

# command for bot to join the channel of the user, if the bot has already joined and is in a different channel, it will move to the channel the user is in
@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

@client.command()
async def quit(ctx):
    voice_client = ctx.voice_client

    if voice_client is not None:
        await voice_client.disconnect()
        await ctx.send('🤙')
    else:
        await ctx.send('😐')

# command to play sound from a youtube URL or spotify URL
@client.command()
async def play(ctx, url):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    # Check if the given url is a Spotify track or playlist
    if "open.spotify.com/track/" in url:
        # Extract the track id from the url
        track_id = url.split("/")[-1]
        # Get the track data from Spotify
        track_data = spotify_api.track(track_id)
        # Set the audio data to the track's preview url
        audio_data = track_data["preview_url"]
        await ctx.send("è possibile solo sentire i 30 secondi di preview di una canzone tramite link di spotify perche spotify è stronzo 😐")
    elif "open.spotify.com/playlist/" in url:
        # Extract the playlist id from the url
        playlist_id = url.split("/")[-1]
        # Get the playlist data from Spotify
        playlist_data = spotify_api.playlist(playlist_id)
        # Get the playlist's track data
        track_data = spotify_api.playlist_tracks(playlist_id)
        # Set the audio data to the first track's preview url
        audio_data = track_data[0]["preview_url"]
        await ctx.send(
            "è possibile solo sentire i 30 secondi di preview di una canzone tramite link di spotify perche spotify è stronzo 😐")
    elif "youtube.com" in url:
        # The url is not a Spotify track or playlist, so use YoutubeDL to extract the audio data
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        audio_data = info['url']
    else:
        await ctx.send('not a link')
    if not voice.is_playing():
        # Play the audio data
        voice.play(FFmpegPCMAudio(audio_data, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send("🎵")
        return

# command to resume voice if it is paused
@client.command()
async def riavvia(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send('restarting')

# command to pause voice if it is playing
@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('paused')

# command to stop voice
@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send('💥💢💥💢')

client.run("YOUR DISCORD BOT TOKEN")

