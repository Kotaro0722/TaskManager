import discord 
from discord import app_commands 

TOKEN="MTE2MjM2ODgyNTgyODg0MzU4MQ.GvwMX6.TeY9VmSdtJ2samVkSQcxHeWiLz21X9-WnrbiKM"


intents = discord.Intents.default() 
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event 
async def on_ready():
  print('ログインしました') 
  # アクティビティを設定 
  new_activity = f"テスト" 
  await client.change_presence(activity=discord.Game(new_activity)) 
  # スラッシュコマンドを同期 
  await tree.sync()
   
@tree.command(name='hw', description='課題の内容と期限を入力してください') 
async def test(interaction: discord.Interaction,content:str,deadline:int): 
  await interaction.response.send_message("【"+content+"】["+str(deadline)+"]")
  
client.run(TOKEN)