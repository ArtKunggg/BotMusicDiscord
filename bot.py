import os
import random
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("❌ คุณต้องอยู่ในห้อง voice ก่อน!")
        return
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send(f"✅ เข้าห้อง {channel} แล้ว!")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 ออกจากห้องแล้ว!")
    else:
        await ctx.send("❌ ยังไม่ได้อยู่ในห้อง voice")

@bot.command()
async def play(ctx):
    if ctx.author.voice is None:
        await ctx.send("❌ คุณต้องอยู่ในห้อง voice ก่อน!")
        return

    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()

    music_folder = "music/"
    songs = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]

    if not songs:
        await ctx.send("❌ ไม่มีไฟล์เพลงในโฟลเดอร์ `music/`")
        return

    song = random.choice(songs)
    path = os.path.join(music_folder, song)

    source = discord.FFmpegPCMAudio(path)
    ctx.voice_client.stop()
    ctx.voice_client.play(source)
    await ctx.send(f"🎶 กำลังเปิดเพลง `{song}`")

@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏹️ หยุดเพลงแล้ว")

bot.run("")
