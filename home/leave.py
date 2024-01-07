import discord
from discord.ext import tasks, commands
from discord.utils import get

import json
import os

from leaveInfo import LeaveDB

class Leave(commands.Cog):
    def __init__(self, bot):
        self.config = json.load(open('config.json'))
        self.bot = bot

    def cog_check(self, ctx):
        self.config = json.load(open('config.json'))
        self.leavedb = LeaveDB(bot=self.bot, guild = ctx.guild)
        return True
    
    
    
    @commands.has_permissions(manage_messages = True)
    @commands.group(name = "exit", invoke_without_command=True)
    async def exit(self, ctx):
        embed = discord.Embed(description = "Choose which part of the leave message you want to change: channel, message", color = discord.Color.blue())
        await ctx.send(embed=embed)

    @exit.command(name = "channel")
    async def channel(self, ctx, *, channel:discord.TextChannel):
        self.leavedb.update_value(column = "channel", value=channel.id)
        embed = discord.Embed(description = f"Changed the welcome channel to {channel}", color = discord.Color.blue())
        await ctx.send(embed=embed)

    @exit.command(name = "message")
    async def message (self, ctx, *, message = "{mention} has left {guild}. :("):
        self.leavedb.update_value(column = "message", value = message)
        channel = self.leavedb._get_channel()
        embed = discord.Embed(description = f"I will send {message} into {channel} whenever a new members joins the server!", color = discord.Color.blue())
        await ctx.send(embed=embed)

    
async def setup(bot):
        await bot.add_cog(Leave(bot))