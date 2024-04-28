import discord
import re
import datetime

TOKEN="MTE2MjM2ODgyNTgyODg0MzU4MQ.GERouF.uswQTOcwMgqZsdlhvnfdJzhsLTsd_w4FHl-zO0"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.typing = False
intents.reactions = True
intents.guilds = True

client = discord.Client(intents=intents)

async def register_task(message:discord.Message):
    this_year = datetime.date.today().year
    date_str = re.findall(r"\d\d?/\d\d?\s\d\d?:\d\d", message.content)[0]
    date = datetime.datetime.strptime(
        f"{this_year}/"+date_str, "%Y/%m/%d %H:%M")
    channel_id = message.channel.id
    channel = message.channel
    print(channel)
    print(channel_id)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    
@client.event
async def on_message(message:discord.Message):
    pattern_task_register = r"【.*】\s*\[\d\d\/\d\d\s\d\d\:\d\d]"
    is_task_register = re.fullmatch(pattern_task_register, message.content)
    if is_task_register:
        await register_task(message)
    
@client.event
async def on_raw_message_edit(payload:discord.RawMessageUpdateEvent):
    print(payload.data["content"])


client.run(token=TOKEN)
