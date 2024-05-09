import discord
import re
import datetime
import config
import pandas
from discord.ext import tasks
from mydblib import my_update
from mydblib2 import my_select

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
    
def select_tomorrow_task(list:pandas.DataFrame):
    today=datetime.datetime.today()
    year=today.year
    month=today.month
    day=today.day
    hour=today.hour
    minute=today.minute
    today=datetime.datetime(year,month,day,hour,minute)
    tomorrow=today+datetime.timedelta(days=1)
    
    ans=[]
    
    if pandas.to_datetime(list["deadline"])==tomorrow:
        ans.append(list)
    return ans

def select_thirty_minutes_later_task(list:pandas.DataFrame):
    today=datetime.datetime.today()
    year=today.year
    month=today.month
    day=today.day
    hour=today.hour
    minute=today.minute
    today=datetime.datetime(year,month,day,hour,minute)
    thirty_minutes_later=today+datetime.timedelta(minutes=30)
    
    ans=[]

    if pandas.to_datetime(list["deadline"])==thirty_minutes_later:
        ans.append(list)
    return ans

def get_thread_member_id(members:discord.ThreadMember):
    id_list=[]
    for member in members:
        id_list.append(member.id)
    return id_list

async def reject_bot_id(guild:discord.Guild,list):
    member_list=[]
    for user_id in list:
          user:discord.Member=await guild.fetch_member(user_id)
          if not user.bot:
              member_list.append(user_id)
    return member_list

async def get_submit_member_id(message:discord.Message):
    reaction_users = []
    for reaction in message.reactions:
        if reaction.emoji=="✅":
            async for user in reaction.users():
                if user not in reaction_users:
                    reaction_users.append(user.id)
    return reaction_users

def get_guild(guild_list,thread_id):
    access_guild=None
    for guild in guild_list:
        if guild.get_channel_or_thread(thread_id):
            access_guild=guild
    return access_guild

def gene_mention(member_list):
    if len(member_list)>0:
        mention_str=""
        for member in member_list:
            mention_str+=f"<@{member}> "
        return mention_str
    else:
        return None

async def remind(data:pandas.Series):
    for element in data:
        guild=get_guild(client.guilds,element[0]["thread_id"])
        thread=await client.fetch_channel(element[0]["thread_id"])
        join_members=await thread.fetch_members()
        join_members_id=get_thread_member_id(join_members)
        class_members_id=await reject_bot_id(guild,join_members_id)
        
        message=await thread.fetch_message(element[0]["message_id"])
        submit_members_id=await get_submit_member_id(message)
        
        unSubmit_members_id=list(set(class_members_id)-set(submit_members_id))
        
        mention=gene_mention(unSubmit_members_id)
        if mention:
            await thread.send(content=mention+f"[課題](<https://discord.com/channels/{guild.id}/{thread.id}/{message.id}>)を出し忘れていませんか？")

@tasks.loop(seconds=60)
async def loop():
    sql_select_task=f"""
        SELECT * FROM {task_table};
    """
    task_list=my_select(dbName,sql_select_task)
    
    tomorrow_task=task_list.apply(select_tomorrow_task,axis=1)
    # await thread.send(cleaned_tomorrow_task)
    cleaned_tomorrow_task=tomorrow_task[tomorrow_task.apply(lambda x:x !=[])]
    await remind(cleaned_tomorrow_task)
    
    thirty_minutes_later_task=task_list.apply(select_thirty_minutes_later_task,axis=1)
    cleaned_thirty_minutes_later_task=thirty_minutes_later_task[thirty_minutes_later_task.apply(lambda x:x !=[])]
    await remind(cleaned_thirty_minutes_later_task)
     
    today=datetime.datetime.today()
    sql_delete_done_task=f"""DELETE FROM {task_table} WHERE deadline<'{today}'"""
    my_update(dbName,sql_delete_done_task)
    
    
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    loop.start()

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
async def on_message(message:discord.Message):
    pattern_task_register = r"【.*】\s*\[\d\d?\/\d\d?\s\d\d?:\d\d?]"
    is_task_register = re.fullmatch(pattern_task_register, message.content)
    if is_task_register:
        await register_task(message)
    
# @client.event
# async def on_raw_message_edit(payload:discord.RawMessageUpdateEvent):
#     print(payload.data["content"])

client.run(token=TOKEN)

