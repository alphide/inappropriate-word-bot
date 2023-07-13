import os
import discord
import discord.utils
import random
import re
from discord import Emoji
from discord.utils import get
from discord.ext import commands
from interactions import GuildIntegrations


intents = discord.Intents.default()
intents.message_content = True
token = os.getenv('DISCORD_TOKEN')
client = commands.Bot(command_prefix = "~", intents=intents)
count = 5
currentTC = ""
ages = False


warning = [
    "No profanity ",
    "Let's not use that kind of language ",
    "Can't believe you kiss your mother with that mouth "
]

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


async def load_cogs():
    for filename in os.listdir('./Discord Bot/cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    await load_cogs()
    print("Up and running {0.user}!".format(client))

    
@client.event
async def on_guild_join(guild):
   id = guild.id
   GuildIntegrations.add(id)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    # check for banned words in message
    '''if any(word in msg.lower() for word in family_list):
        await message.delete()
        await message.channel.send("No talking about our parents 😓", delete_after=3)
    if any(word in msg.lower() for word in badlist):
        await message.delete()
        await message.channel.send(random.choice(warning) + "{}".format(message.author.mention),
                                   delete_after=3)  # sends a random value(phrase) in warning list and deletes the message subsequently
    '''

    '''if message.author.id == 143161456119119872:
     # Replace with the user ID you want to add a reaction to
        emoji = discord.utils.get(client.emojis, name='FeelsSpecialMan') # Replace with the name of your custom emoji
        if emoji:
            await message.add_reaction(emoji) '''
    if "Muted" in [role.name for role in message.author.roles]:
        await message.delete()
    

    '''if message.author == client.user:
        return
    elif message.content.startswith('~'):
        return
    else:
        words = re.findall(r'\w+|[^\w\s]', message.content)
        last_word = ""
        for i in range(len(words) - 1, -1, -1):
            if words[i].isalpha():
                last_word = words[i]
                break
        if last_word != "":
            emoji = get(message.guild.emojis, name="OMEGALUL")
            new_last_word = last_word + "ages"
            new_message = message.content.rsplit(
                last_word, 1)[0] + new_last_word + " OMEGALUL " + str(emoji)
            await message.channel.send(new_message)
    '''
    await client.process_commands(message)  # so that on_message does not interfere with any other commands



client.run(token)
