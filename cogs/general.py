import asyncio
from logging import warning
import random
import time
import discord
import discord.utils
import openai
import requests
import json

from io import BytesIO
from discord.ext import commands
from discord.ext.commands import has_permissions
from sys import platform



with open("./Discord Bot/config.json", "r") as f:
    config = json.load(f)

with open("./Discord Bot/cookie.txt", 'r') as f:
    cookieTxt = f.read()

class General(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.servers = {}
        self.cookie = cookieTxt
        self.userAgent = config["userAgent"]


    @commands.command(pass_context=True, aliases=['c', 'C'])
    @has_permissions(manage_messages=True,
                     manage_roles=True)  
    async def clearmsg(self, ctx, num=100):
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
        return

    @commands.command(pass_context=True, aliases=['ar'])
    @has_permissions(manage_messages=True, manage_roles=True)
    async def role(self, ctx, user: discord.Member, role: discord.Role):
        if role in user.roles:
            await ctx.send(f'{user.mention} already has this role!')
        else:
            await user.add_roles(role)
            await ctx.send(f'{role.mention} has been given to {user.mention}')
        return
    @commands.command(pass_context=True, aliases=['rr'])
    @has_permissions(manage_messages=True, manage_roles=True)
    async def removerole(self, ctx, user: discord.Member, role: discord.Role):
        if role not in user.roles:
            await ctx.send(f'{user.mention} did not have {role.mention} to begin with!')
        else:
            await user.remove_roles(role)
            await ctx.send(f'{role.mention} has been removed from {user.mention}')
        return
    @commands.command()
    @has_permissions(manage_messages=True, manage_roles=True)
    async def mute(self, ctx, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await user.add_roles(role)
        await ctx.send(f"{user.mention} has been muted")
        return

    @commands.command()
    @has_permissions(manage_messages=True, manage_roles=True)
    async def unmute(self, ctx, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await user.remove_roles(role)
        await ctx.send(f"{user.mention} has been unmuted")
        return

    @commands.command()
    async def test(self, ctx):
        await ctx.send("Jonathan's bot, WIP")
        return
    """
    @commands.command()
    @has_permissions(manage_messages=True, manage_roles=True)
    async def addword(self, ctx, word: str):
        server_id = str(ctx.guild.id)
        if server_id not in self.servers and word not in badlist:
            self.servers[server_id] = []
        else:
            self.servers[server_id].append(word)
            await ctx.send(f"Added {word} to the list!")
        return
    
    @commands.command()
    @has_permissions(manage_messages=True, manage_roles=True)
    async def removeword(self, ctx, word: str):
        server_id = str(ctx.guild.id)
        if server_id in self.servers and word in badlist:
            self.servers[server_id].remove(word)
        else:
            await ctx.send(f"{word} is not in the list!")
        return
"""
    
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ask(self, ctx):
        await ctx.send("What would you like to know?")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        response_message = await self.bot.wait_for('message', check=check)

        # call OpenAI API to process user question
        
        response = openai.Completion.create(
                model = "text-davinci-003",
                prompt=response_message.content,
                max_tokens=100
            )
        # send response back to Discord user
        await ctx.send(response.choices[0].text.replace("\n", " "))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def image(self, ctx):
        await ctx.send("What image would you like to generate?")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            response_message = await asyncio.wait_for(self.bot.wait_for('message', check=check), timeout=10.0)
        except asyncio.TimeoutError:
            await ctx.send("You took too long...")
            return

        loading_message = await ctx.send("Generating <a:2923printsdark:1084765439734853674>")
        
        try:
            response = openai.Image.create(
                prompt=response_message.content,
                n=1,
                size="256x256"
            )
            
            image_url = response['data'][0]['url']
            image_content = requests.get(image_url).content
            image_file = BytesIO(image_content)
            await loading_message.edit(content="Image generated \u2705")
            await ctx.send(file=discord.File(fp=image_file, filename='image.png'))
        except:
            await ctx.send(random.choice(warning))
"""
    @commands.command(name='chegg', help='Get answers from a Chegg link')
    async def chegg(self, ctx, url: str):
        answer = await self.fetch_chegg(url)
        await ctx.send(answer)
   
    async def fetch_chegg(self, url: str) -> str:
        user_agent = UserAgent()
        chrome_options = Options()
        chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument(f"user-agent={user_agent.random}")
        # chrome_options.add_argument('--disable-blink-features=AutomationControlled')   

        browser = webdriver.Chrome(options=chrome_options)
        browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        browser.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})

        login_url = 'https://www.chegg.com/auth'
        browser.get(login_url)
        delay = random.uniform(1, 5)
        
        email_input = browser.find_element(By.ID, 'login_email_input')
        email_input.send_keys(chegg_email)
        time.sleep(delay)

        password_input = browser.find_element(By.ID, 'login_password_input')
        password_input.send_keys(chegg_password)
        time.sleep(delay)

        sign_in_button = browser.find_element(By.CSS_SELECTOR, 'button[data-test="login_submit_button"]')
        sign_in_button.click()

        time.sleep(delay)
        browser.get(url)
        time.sleep(delay)

        soup = BeautifulSoup(browser.page_source, 'html.parser')
        browser.quit()

        answer_section = soup.find('div', {'data-test': 'qna-html-answer-content'})
        if answer_section:
            answer_text = answer_section.get_text(separator='\n').strip()
            return answer_text
        else:
            return "No answer found."
        """ 
    
async def setup(bot):
    await bot.add_cog(General(bot))