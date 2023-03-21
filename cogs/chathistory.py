import asyncio
import datetime
import discord
import sqlite3
import json
import io
from discord.ext import commands
from datetime import datetime

class ChatHistory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect('chat_history.db')
        self.db.execute('''CREATE TABLE IF NOT EXISTS messages
            (message_id INTEGER PRIMARY KEY,
            channel_id INTEGER,
            author_id INTEGER,
            author_name TEXT,
            content TEXT,
            timestamp INTEGER,
            image_attachments TEXT
            )''')

        self.db.commit()
        


    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return  # Ignore messages sent by bots
        
        attachment_urls = []
        for attachment in message.attachments:
            # Check if the attachment is an image file
            if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4')):
                attachment_url = attachment.url
                attachment_urls.append(attachment_url)
        
        
    # insert the message and its attachments (if any) into the database
        self.db.execute('''INSERT INTO messages
            (message_id, channel_id, author_id, author_name, content, timestamp, image_attachments)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (message.id, message.channel.id, message.author.id, message.author.name, message.content, message.created_at.timestamp(), ', '.join(attachment_urls)))

        self.db.commit()



    @commands.command()
    async def history(self, ctx, page_number=1):
        messages_per_page = 10
        page_number = max(page_number, 1)  # Ensure that page number is at least 1
        num_messages = self.db.execute('SELECT COUNT(*) FROM messages WHERE channel_id = ?', (ctx.channel.id,)).fetchone()[0]
        num_pages = (num_messages + messages_per_page - 1) // messages_per_page  # Calculate number of pages
        start_index = (page_number - 1) * messages_per_page
        end_index = start_index + messages_per_page
        messages = self.db.execute('''SELECT author_name, author_id, content, timestamp, image_attachments FROM messages
                                    WHERE channel_id = ?
                                    ORDER BY message_id DESC
                                    LIMIT ?, ?''',
                                    (ctx.channel.id, start_index, messages_per_page)).fetchall()

        embed = discord.Embed(title="**Chat History**", color=discord.Color.blue())
        
        for message in messages:
                timestamp = datetime.fromtimestamp(message[3]).strftime('%Y-%m-%d %H:%M:%S')
                embed.add_field(name=f"{message[0]} - ({timestamp})", value=message[2], inline=False)

                attachment_urls = message[4].split(',') if message[4] else []
                for attachment_url in attachment_urls:
                    if attachment_url:
                        embed.add_field(name='Image Attachment', value=attachment_url, inline=False)
    
        embed.set_footer(text=f"Page {page_number} of {num_pages}")

        if page_number > 1:
            embed.set_author(name="Previous Page", icon_url="https://cdn.discordapp.com/emojis/859343410174283786.png?v=1")
        if page_number < num_pages and (not page_number == 1 and not page_number == num_pages):
            embed.add_field(name="\u200b", value="\u200b", inline=False)
            embed.set_author(name="Next Page", icon_url="https://cdn.discordapp.com/emojis/859343443212644116.png?v=1")
        

        message = await ctx.send(embed=embed)
        
        if num_pages > 1:
            await message.add_reaction("⬅️")
            await message.add_reaction("➡️")

            def check(reaction, user):
                return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ["⬅️", "➡️"]
            
            prev_message_id = message.id
            while True:
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                    if str(reaction.emoji) == "⬅️":
                        page_number -= 1
                    elif str(reaction.emoji) == "➡️":
                        page_number += 1

                    page_number = max(page_number, 1)
                    page_number = min(page_number, num_pages)

                    start_index = (page_number - 1) * messages_per_page
                   
                    messages = self.db.execute('''SELECT author_name, author_id, content, timestamp, image_attachments FROM messages
                                                WHERE channel_id = ?
                                                ORDER BY message_id DESC
                                                LIMIT ?, ?''',
                                                (ctx.channel.id, start_index, messages_per_page)).fetchall()
                    
                    embed = discord.Embed(title="**Chat History**", color=discord.Color.blue())
                    
                    for message in messages:

                            timestamp = datetime.fromtimestamp(message[3]).strftime('%Y-%m-%d %H:%M:%S')
                            embed.add_field(name=f"{message[0]} - ({timestamp})", value=message[2], inline=False)

                            attachment_urls = message[4].split(',') if message[4] else []
                            for attachment_url in attachment_urls:
                                if attachment_url:
                                    embed.add_field(name='Image Attachment', value=attachment_url, inline=False)
                    embed.set_footer(text=f"Page {page_number} of {num_pages}")

                    
                    message = await ctx.send(embed=embed)

                    await message.remove_reaction(reaction, user)
                    if page_number > 1:
                        await message.add_reaction("⬅️")
                    if page_number < num_pages:
                        await message.add_reaction("➡️")
                    
                    try:
                        previous_message = await ctx.channel.fetch_message(prev_message_id)
                        await previous_message.delete()
                    except Exception as e:
                        print(e)
                 
                    prev_message_id = message.id
                except asyncio.TimeoutError:
                    await message.clear_reactions()
                    await message.delete()
                    break
    def __unload(self):
        self.db.close()

async def setup(bot):
    await bot.add_cog(ChatHistory(bot))