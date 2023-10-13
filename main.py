import discord
from discord.ext import commands
import sqlite3

TOKEN="MTE2MjM2ODgyNTgyODg0MzU4MQ.GvwMX6.TeY9VmSdtJ2samVkSQcxHeWiLz21X9-WnrbiKM"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

bot=commands.Bot(command_prefix="/",intents=intents)



@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    
@bot.command()
async def test(ctx,arg):
    await ctx.send(arg)

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith(''):
#         await message.channel.send('Hello!')

client.run(token=TOKEN)
