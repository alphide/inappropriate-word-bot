import os
import random
from discord.ext import commands
from discord.ext.commands import has_permissions
from replit import db
from words_list import list


client = commands.Bot(command_prefix = "~")
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

  # myid = '247715665933369346', personal user id for owner-only commands

  if db["responding"]: # 
    ''' 
    local var for on messsage commands
    '''  
    hasPerms = message.author.permissions_in(message.channel).manage_messages # permissions check in order to run certain commands (ex: enabling and disabling bot)

    if msg.startswith('~test'): # command to see if bot is running
      await message.channel.send("Jonathan's Bot! Work in progress!")

    if any(word in msg.lower() for word in list):
      await message.delete()
      await message.channel.send(random.choice(warning) + "{}".format(message.author.mention), delete_after=3) # sends a random value(phrase) in warning list and deletes the message subsequently

    # enables and disables the bot
    if msg == ("~enable") and hasPerms:
      db["responding"] = True
      await message.channel.send("BL33P! is enabled")

    if msg == ("~disable") and hasPerms:
      db["responding"] = False
      await message.channel.send("BL33P! is disabled")

  await client.process_commands(message) # so that on_message does not interfere with any other commands
    

@client.command(pass_context=True, aliases=['c', 'C'])
@has_permissions(manage_messages=True,
                 manage_roles=True)  # decorator so that only users with certain permissions can run the command
async def clearmsg(ctx, num=100):
    channel = ctx.message.channel
    msgs = []
    # appends the messages in msgs list
    async for i in channel.history(limit=num + 1):  # deletes own command message
        msgs.append(i)

    await channel.delete_messages(msgs)  # deletes msgs list
    if num == 1:
        await ctx.send(f'{num} message has been cleared by {ctx.message.author.mention}', delete_after=3)
    else:
        await ctx.send(f'{num} messages have been cleared by {ctx.message.author.mention}', delete_after=3)


@client.command(pass_context=True, aliases=['ar'])
@has_permissions(manage_messages=True, manage_roles=True)
async def role(ctx, user: discord.Member, role: discord.Role): 
    if role in user.roles:
        await ctx.send(f'{user.mention} already has this role!')
    else:
        await user.add_roles(role)
        await ctx.send(f'{role.mention} has been given to {user.mention}')


@client.command(pass_context=True, aliases=['rr'])
@has_permissions(manage_messages=True, manage_roles=True)
async def removerole(ctx, user: discord.Member, role: discord.Role):
    if role not in user.roles:
        await ctx.send(f'{user.mention} did not have {role.mention} to begin with!')
    else:
        await user.remove_roles(role)
        await ctx.send(f'{role.mention} has been removed from {user.mention}')


@client.command()
@has_permissions(manage_messages=True, manage_roles=True)
async def mute(ctx, user: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await user.add_roles(role)
    await ctx.send(f"{user.mention} has been muted")


@client.command()
@has_permissions(manage_messages=True, manage_roles=True)
async def unmute(ctx, user: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await user.remove_roles(role)
    await ctx.send(f"{user.mention} has been unmuted")
    
client.run(token)


