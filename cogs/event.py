import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class Events(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'디스코드 봇 로그인이 완료되었습니다.')

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.guild is not None:
            logger.info(f"({ctx.guild} | {ctx.channel} | {ctx.author}) {ctx.message.content}")
        else:
            logger.info(f"(DM채널 | {ctx.author}) {ctx.message.content}")

    @commands.Cog.listener()
    async def on_command_error(self, _, error):
        if error.__class__ == discord.ext.commands.errors.CommandNotFound:
            return
        raise error


def setup(client):
    client.add_cog(Events(client))
