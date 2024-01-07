import discord
from discord.ext import tasks, commands
from discord.utils import get
import asyncio

import json
import os

from prefixInfo import PrefixDB


class Prefix(commands.Cog):
    def __init__(self, bot):
        self.config = json.load(open('config.json'))
        self.bot = bot

    def cog_check(self, ctx):
        self.config = json.load(open('config.json'))
        return True

    

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def prefix(self, ctx, *, pre = "="):
        prefix_db = PrefixDB(bot = self.bot, guild = ctx.guild)
        prefix_db._create_new_prefix()
        prefix_db.update_value(column="prefix", pre=pre)
        await ctx.send(f"Changed the prefix to {pre}")

async def setup(bot):
    await bot.add_cog(Prefix(bot))