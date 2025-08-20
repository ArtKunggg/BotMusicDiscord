import os
import random
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    activity = discord.Activity(type=discord.ActivityType.listening, name="วิธีใช้ | !help")
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("❌ คุณต้องอยู่ในห้อง voice ก่อน!")
        return
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send(f"✅ เข้าห้อง {channel} แล้ว!")

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
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()  # หยุดเพลงปัจจุบัน

        # หาไฟล์เพลงใหม่
        music_folder = "music/"
        songs = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]

        if not songs:
            await ctx.send("❌ ไม่มีไฟล์เพลงในโฟลเดอร์ `music/`")
            return

        song = random.choice(songs)
        path = os.path.join(music_folder, song)

        source = discord.FFmpegPCMAudio(path)
        ctx.voice_client.play(source)

        await ctx.send(f"⏭️ ข้ามเพลง กำลังเล่น `{song}`")
    else:
        await ctx.send("❌ ตอนนี้ไม่มีเพลงที่กำลังเล่นอยู่")


@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏹️ หยุดเพลงแล้ว")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 ออกจากห้องแล้ว!")
    else:
        await ctx.send("❌ ยังไม่ได้อยู่ในห้อง voice")

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="🎵 วิธีการใช้งานบอทเพลง",
        description="รวมคำสั่งที่คุณสามารถใช้ได้",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="✅ เข้าห้อง",
        value="`!join` - นำบอทเข้าห้อง",
        inline=False
    )
    embed.add_field(
        name="▶️ เล่นเพลง",
        value="`!play` - สุ่มเปิดเพลงจากโฟลเดอร์",
        inline=False
    )

    embed.add_field(
    name="⏭️ ข้ามเพลง",
    value="`!skip` - ข้ามไปเพลงถัดไป",
    inline=False
    )

    embed.add_field(
        name="⏹️ หยุดเพลง",
        value="`!stop` - หยุดเพลง",
        inline=False
    )

    embed.add_field(
        name="❌ ออกจากห้อง",
        value="`!leave` - ออกจากห้อง",
        inline=False
    )

    embed.add_field(
        name="ℹ️ วิธีใช้งาน",
        value="`!help` - แสดงข้อความช่วยเหลือ",
        inline=False
    )

    embed.set_footer(text="Made with ❤️ by MASTERART")

    await ctx.send(embed=embed)

bot.run("")
