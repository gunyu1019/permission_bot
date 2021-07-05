import os
import discord
import json
from discord.ext import commands
from discord.http import Route

from module.components import ActionRow, Button, Selection


class Command(commands.Cog, name="기본 명령어"):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.color = 0x0070ff
        self.directory = os.path.dirname(os.path.abspath(__file__)).replace("\\cogs", "")
        self.BASE_URL = "https://discord.com/api/oauth2/authorize?client_id={bot_id}&permissions={permission}&scope=bot"

    @commands.command(aliases=['권한'])
    async def permission(self, ctx: commands.Context, bot_id: int = None):
        if bot_id is None:
            bot_id = self.bot.user.id
        embed = discord.Embed(
            title="Discord Bot Invite",
            description="Put in the permission you want and click the link."
        )
        x_emoji = discord.PartialEmoji(name="❌")
        embed.add_field(name="Permitted permissions", value=f"{x_emoji}", inline=True)

        with open(os.path.join(self.directory, "permission.json"), "r") as file:
            option = json.load(file).get("General", [])

        data = {
            "embed": embed.to_dict(),
            "components": [
                ActionRow([
                    Selection(
                        custom_id="General",
                        options=option,
                        placeholder="Choose a permission",
                        max_values=len(option)
                    ).to_dict()
                ]).to_dict(), ActionRow([
                        Button(label="General", style=1, custom_id="General", disabled=True).to_dict(),
                        Button(label="Text", style=1, custom_id="TextChannel").to_dict(),
                        Button(label="Voice", style=1, custom_id="VoiceChannel").to_dict(),
                        Button(label="Link!", style=5, url=self.BASE_URL.format(bot_id=bot_id, permission=0)).to_dict()
                ]).to_dict()
            ]
        }

        route = Route('POST', '/channels/{channel_id}/messages', channel_id=ctx.channel.id)
        await self.bot.http.request(route, json=data)
        return


def setup(client):
    client.add_cog(Command(client))
