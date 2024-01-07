import discord
from discord.ext import commands
from discord.utils import get
import asyncio

import openai
from datetime import datetime

import os
import traceback
import json

from welcomeInfo import WelcomeDB
from prefixInfo import PrefixDB
from roleInfo import RoleDB 
from gifInfo import GifDB
from leaveInfo import LeaveDB
from gptInfo import GPTdb

openai.api_key = "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"

def get_completion(prompt, model = 'gpt-3.5-turbo'):
    new_prompt = f"Would you consider anything of the following to be hateful, derogatory, a slur, misinformation, or a swear word. Answer with yes or no, do not answer with anything other than yes or no: {prompt}"
    messages = [{"role": "user",
                 "content": new_prompt}]
    response = openai.ChatCompletion.create(
        model = model,
        messages = messages,
        temperature = 0
    )

    return response.choices[0].message["content"]


config = json.load(open('config.json'))


def get_prefix (bot, message):
    prefix_db = PrefixDB(bot=bot, guild=message.guild)
    if not message.guild:
        return commands.when_mentioned_or("=")(bot, message)
    
    prefix = prefix_db._get_prefix()
    return prefix

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = get_prefix, case_insensitive=True, intents=intents)


bot.home_dir = os.getcwd()
bot.config = json.load(open('config.json'))
bot.token = bot.config["Token"]



initial_extensions = [
    "moderation",  
    "prefix",
    "server",
    "leave"
]
 
async def load_extension():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}")
            traceback.print_exc()

asyncio.run(load_extension())

@bot.event
async def on_message(message):
    prefix_db = PrefixDB(bot=bot, guild=message.guild)
    if f"<@!{bot.user.mention}" in message.content:
        if str(message.guild.id) in prefix_db._get_prefix():
            prefix = prefix_db._get_prefix()
        else:
            prefix = "="
        await message.channel.send(f"My prefix here is {prefix}")

    await bot.process_commands(message)

    gpt_db = GPTdb(bot=bot, guild=message.guild)
    bool = gpt_db._get_bool()
    if int(bool) == 1:      
        response = get_completion(message.content)
        if "yes" in response.lower():
            await message.delete()
    
    

@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "\n")
    print(f"Running on version {discord.__version__}")

@bot.event
async def on_member_join(member):
    welcome = WelcomeDB(bot = bot, guild = member.guild)
    gif = GifDB(bot=bot, guild = member.guild)
    role = RoleDB(bot=bot, guild = member.guild)
    raw_welcome_channel = welcome._get_welcome_channel()
    welcome_channel = bot.get_channel(raw_welcome_channel)
    welcome_message = welcome._get_welcome_message()

    welcome_gif = gif._get_gif()

    mention = member.mention
    user = member.name
    guild = member.guild

    rolebool = role._get_bool()
    if rolebool == 1:
        role1 = role._get_role()
        autorole = get(member.guild.roles, name = role1)
        await member.add_roles(autorole)


    embed = discord.Embed(color = discord.Color.blue(), description=str(welcome_message).format(mention=mention, user = user, guild = guild))
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name=member.name, icon_url=member.avatar_url)
    embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
    embed.set_image(url=welcome_gif)
    embed.timestamp = datetime.utcnow()

    await welcome_channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    leave = LeaveDB(bot=bot, guild=member.guild)
    message = leave._get_message()
    channel = leave._get_channel()
    leave_channel = bot.get_channel(channel)
    
    mention = member.mention
    user = member.name
    guild = member.guild
    
    embed = discord.Embed(color = discord.Color.blue(), description=str(message).format(mention=mention, user = user, guild = guild))
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name=member.name, icon_url=member.avatar_url)
    embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
    embed.timestamp = datetime.utcnow()

    await leave_channel.send(embed=embed)



@bot.command()
async def status(ctx, *, status):
    if ctx.author.id == 349256335742730253:
        await bot.change_presence(activity=discord.Game(name=status))
        await ctx.send(f"Changed Bot's status to {status}")




bot.run(bot.token)