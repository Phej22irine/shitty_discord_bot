#import private
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random
import webbrowser
import winsound
import time
from scripts import servercommands
from scripts import data_validation
#from scripts import gameboy

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents= intents)

cinema_list = ["https://static.wikia.nocookie.net/megapedia/images/2/23/Absolute_Cinema.png/revision/latest/scale-to-width-down/732?cb=20250921020702",
               "https://www.anhnghethuatdulich.com/wp-content/uploads/2025/09/anh-meme-tuyet-doi-dien-anh-meo-tong-tai.jpg",
               "https://i.pinimg.com/1200x/ff/62/0d/ff620d710aa8a1207d9362d1e945435a.jpg",
               "https://i.pinimg.com/236x/ea/67/1f/ea671f9a285062e9a5141d8022bc77ce.jpg",
               "https://i.kym-cdn.com/entries/icons/original/000/043/589/FTjzOCUWUAEqROW.jfif"]


@bot.event
async def on_ready(): print(f"{bot.user.name} is ready.")
    
@bot.event
async def setup_hook(): data_validation.check_date.start()


@bot.event
async def on_message(message):
    if message.author == bot.user: return
    check_slurs = servercommands.slurchecker(message.content.lower(), message.author.mention)
    
    if check_slurs[0] == True:
        author_slurs = data_validation.update_slurs(str(message.author.id), int(check_slurs[2]))
        await message.channel.send("@everyone, " + check_slurs[1] + f"\n{message.author.mention} has said a total of {author_slurs[0]} slurs.")
    
        if author_slurs[1]:
            await message.channel.send(f"@everyone, {message.author.mention} has mention over a hundred slurs! give him a round of applause!")
    
    if "cinema" in message.content.lower():
        embed = discord.Embed(title="Absolute Cinema!")
        embed.set_image(url=random.choice(cinema_list))
        await message.channel.send(embed=embed)
    await bot.process_commands(message)

@bot.command()
async def rndmbsgo(ctx, *, msg):
    await ctx.reply(servercommands.translatecommands(msg))

@bot.command()
async def cornyahh(ctx):
    embed = discord.Embed()
    embed.set_image(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRoFzXk76p_VO11q5GI3mI1438cLdogWgbCVA&s")
    await ctx.reply(embed = embed)
    
@bot.command()
async def peak(ctx):
    embed = discord.Embed()
    embed.set_image(url="https://media0.giphy.com/media/v1.Y2lkPWFlZWNjYzExcGxmZ2c3dTM0cnhmMnNocWx1a3dwMWg5eGE0dGhtajJhcHpydDIyYyZlcD12MV9naWZzX2dpZklkJmN0PWc/PAZWqoSDU1KMgGvjiK/200.gif")
    await ctx.reply(embed = embed)

@bot.command()
async def nightreign(ctx):
    await ctx.reply(f"<@{1023493956622876733}>\n<@{831831940462149682}>\n<@{768102905172983808}>\n<@{479992071655260160}>\n<@{761214087220428851}>")

# Random NHen codes
@bot.command()
async def randomsabaw(ctx):
    validate_data = data_validation.goon_counter(str(ctx.message.author.id))
    
    if validate_data[0] == True:
        await ctx.reply(f"https://nhentai.net/g/{random.randint(50000, 60000)}")
        await ctx.reply(f"You have {validate_data[1]} searches remaining.")
    
    if validate_data[1] == 0:
        await ctx.reply(f"you have used all your goon points, ya fucking gooner.")


@bot.command()
async def sabaw(ctx, msg):
    if str(msg).isdigit():
        for i in range(0, int(msg)):
            validate_data = data_validation.goon_counter(str(ctx.message.author.id))
    
            if validate_data == False: break
    
            await ctx.reply(f"https://nhentai.net/g/{random.randint(50000, 600000)}")
        await ctx.reply(f"You have {validate_data[1]} searches remaining.")        

    if validate_data[1] == 0:
        await ctx.reply(f"you have used all your goon points, ya fucking gooner.")


@bot.command()
async def update_users(ctx):
    data_validation.update_userdata()
    await ctx.reply("done!")

@bot.command()
async def randomahhlink(ctx, link):
    
    # Get channel url
    video_url = link.replace("\"", "\\\"")
    webbrowser.open(video_url)



@bot.command()
async def snedshi(ctx, link):
    link = "https://discord.com/channels/1246151460899520512/1485255333579325511"
    webbrowser.open(link)

timer = 0
@bot.command()
async def magic(ctx):
    await ctx.channel.send("Shutting down Paul's Laptop. Hasta la vista, baby!\n\nAny last words?")
    timer = 10
    winsound.PlaySound('shutting_down.wav', winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)
    os.system("shutdown /r /t 16")
    
    while True:
        await ctx.channel.send(f"reboot down in: {timer} seconds")
        timer -= 1
        time.sleep(1)
        
        if timer <= 0: break
    
    await ctx.channel.send("Goodbye.")


"""
@bot.command()
async def gggg(ctx, *,msg):
    gameboy.game_input(msg)
"""
in_call = None
@bot.command()
async def fah(ctx): await play_sound(ctx, 'sounds/fah.mp3')
    
@bot.command()
async def boom(ctx): await play_sound(ctx, 'sounds/vine.mp3')

@bot.command()
async def sus(ctx): await play_sound(ctx, 'sounds/sus.mp3')

@commands.command()
async def joincall(ctx):
    global in_call
    
    if ctx.author.voice:
        channel = ctx.author.voice.channel
    
        # Connect to voice channel
        try:
            voice_client = await channel.connect()
            in_call = voice_client
        except: print("in call")
    
    return voice_client

async def play_sound(ctx, snd):
    await joincall(ctx)
    global in_call
    
    # Play local file
    source = discord.FFmpegPCMAudio(snd)
    in_call.play(source)

@bot.command()
async def disco(ctx):
    await in_call.disconnect()

bot.run(token, log_handler= handler, log_level=logging.DEBUG)