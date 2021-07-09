import discord
import os
import time
import random
from discord.ext import commands
from replit import db
from words_list import list
from datetime import datetime


client = discord.Client()
token = os.environ['token']

warning = [
  "No profanity ", "Let's not use that kind of language ", "Can't believe you kiss your mother with that mouth "
  ]

if "responding" not in db.keys():
  db['responding'] = True

@client.event
async def on_ready():
  print("Up and running {0.user}!".format(client))

@client.event
async def on_message(message):
  if message.author == client.user: 
    return 

  msg = message.content
  # myid = '247715665933369346'

  if db["responding"]:
    ''' 
    local var for on messsage commands
    '''  
    count = 0
    # opens spam_detection to strip white space and check if equal to the user's id
    '''with open("spam_detection.txt", "r+") as file:
      for i in file:
        if i.strip("\n") == str(message.author.id):
          count += 1

    file.writelines(f"{str(message.author.id)}\n")
    
    if count > 5 and not message.author.guild_permissions.administrator:
      await message.channel.purge(after=datetime.now() - datetime.timedelta(hours=1), check = lambda x: x.author.id == message.author.id, oldest_first=False)
      muted_role = discord.utils.get(discord.guild.roles, name="Muted")
      await message.author.add_roles(muted_role)'''

    if message.content.startswith('~test'): # command to see if bot is running
      await message.channel.send("Jonathan's Bot! Work in progress!")

    if any(word in msg.lower() for word in list):
      await message.delete()
      await message.channel.send(random.choice(warning) + "{}".format(message.author.mention), delete_after=3) # sends a random value(phrase) in warning list and deletes the message subsequently
     

  if msg == ("~enable"): # enables the bot if user types 
    db["responding"] = True
    await message.channel.send("BL33P! is enabled")

  elif msg == ("~disable"):
  
    db["responding"] = False
    await message.channel.send("Bl33P! is disabled")


client.run(token)


