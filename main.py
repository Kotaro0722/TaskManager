import discord
import re
import datetime
import config
from mydblib import my_update

TOKEN=config.TOKEN

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.typing = False
intents.reactions = True
intents.guilds = True

client = discord.Client(intents=intents)

dbName=config.DBNAME
task_table=config.TASK_TABLE

async def register_task(message:discord.Message):
    try:
        thread_id = message.channel.id
        message_id = message.id
        
        today=datetime.date.today()
        year = today.year
        date_str = re.findall(r"\d\d?/\d\d?\s\d\d?:\d\d", message.content)[0]
        temp_date=datetime.datetime.strptime(date_str,"%m/%d %H:%M")
        if today.month>temp_date.month:
            year+=1
        date_str = re.findall(r"\d\d?/\d\d?\s\d\d?:\d\d", message.content)[0]
        date = datetime.datetime.strptime(
            f"{year}/"+date_str, "%Y/%m/%d %H:%M")
        
        sql_insert_data=f"INSERT INTO {task_table}(message_id,thread_id,deadline) VALUES({message_id},{thread_id},'{date}')"
        my_update(dbName,sql_insert_data)
        
        await message.add_reaction("⭕")
        
    except Exception as e:
        print(e) 
    
    

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    
@client.event
async def on_message(message:discord.Message):
    pattern_task_register = r"【.*】\s*\[\d\d?\/\d\d?\s\d\d?:\d\d?]"
    is_task_register = re.fullmatch(pattern_task_register, message.content)
    if is_task_register:
        print("reg pass")
        await register_task(message)
    
@client.event
async def on_raw_message_edit(payload:discord.RawMessageUpdateEvent):
    print(payload.data["content"])


client.run(token=TOKEN)
