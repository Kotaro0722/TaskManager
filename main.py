import discord
import sqlite3

TOKEN="MTE2MjM2ODgyNTgyODg0MzU4MQ.GvwMX6.TeY9VmSdtJ2samVkSQcxHeWiLz21X9-WnrbiKM"

intents = discord.Intents.default()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(token=TOKEN)