import os
import json
import logging
import discord
from discord.ext import commands
from discord.http import Route
from urllib.parse import urlparse, parse_qs

from module.components import ActionRow, Button, Selection, from_payload

logger = logging.getLogger(__name__)


def check_url(url: str):
    parse_data = urlparse(url)
    query = parse_qs(parse_data.query)

    return query.get("client_id")[0], int(query.get("permissions")[0])


def calculate_permission(code: int, permission_fp: dict) -> list:
    return [j.get("label") for i in permission_fp.keys() for j in permission_fp[i] if int(j.get("value"), 16) & code]


def get_permission_value(code: int, permission_file: dict):
    permission_list = calculate_permission(code, permission_file)
    if len(permission_list) == 0:
        x_emoji = discord.PartialEmoji(name="❌")
        return str(x_emoji)
    else:
        check_emoji = discord.PartialEmoji(name="✅")
        permitted = ""
        for i in permission_list:
            permitted += "{} {}\n".format(check_emoji, i)
        return permitted


class Socket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.directory = os.path.dirname(os.path.abspath(__file__)).replace("\\cogs", "")
        self.BASE_URL = "https://discord.com/api/oauth2/authorize?client_id={bot_id}&permissions={permission}&scope=bot"

    @commands.Cog.listener()
    async def on_socket_response(self, payload: dict):
        d = payload.get("d", {})
        t = payload.get("t", "")

        if t == "PRESENCE_UPDATE":
            return

        logger.debug(payload)

        if t == "INTERACTION_CREATE":
            data = d.get("data", {})
            message = d.get("message", {})

            interaction_id = d.get("id")
            interaction_token = d.get("token")
            route = Route(
                'POST',
                '/interactions/{id}/{token}/callback',
                id=interaction_id, token=interaction_token
            )
            edit_route = Route(
                'PATCH',
                '/channels/{channel_id}/messages/{message_id}',
                channel_id=message.get("channel_id"), message_id=message.get("id")
            )
            interaction_data = {
                "type": 6
            }
            await self.bot.http.request(route, json=interaction_data)

            if d.get("type") == 3:
                embed = discord.Embed(
                    title="Discord Bot Invite",
                    description="Put in the permission you want and click the link."
                )

                with open(os.path.join(self.directory, "permission.json"), "r") as file:
                    option = json.load(file)

                edited_message = {
                    "embed": {},
                    "components": []
                }
                components = from_payload(message.get("components"))

                if data.get("component_type") == 2:
                    custom_id = data.get("custom_id")

                    option_data = []
                    if custom_id == "General":
                        option_data = option.get("General")
                    elif custom_id == "TextChannel":
                        option_data = option.get("TextChannel")
                    elif custom_id == "VoiceChannel":
                        option_data = option.get("VoiceChannel")

                    edited_message["components"].append(ActionRow([
                        Selection(
                            custom_id=custom_id,
                            options=option_data,
                            placeholder="Choose a permission",
                            max_values=len(option_data)
                        ).to_dict()
                    ]).to_dict())

                    link_button: Button = components[1].components[3]
                    bot_id, permission = check_url(link_button.url)

                    if custom_id == "General":
                        edited_message["components"].append(ActionRow([
                            Button(label="General", style=1, custom_id="General", disabled=True).to_dict(),
                            Button(label="Text", style=1, custom_id="TextChannel").to_dict(),
                            Button(label="Voice", style=1, custom_id="VoiceChannel").to_dict(),
                            Button(
                                label="Link!",
                                style=5,
                                url=self.BASE_URL.format(bot_id=bot_id, permission=permission)
                            ).to_dict()
                        ]).to_dict())
                    elif custom_id == "TextChannel":
                        edited_message["components"].append(ActionRow([
                            Button(label="General", style=1, custom_id="General").to_dict(),
                            Button(label="Text", style=1, custom_id="TextChannel", disabled=True).to_dict(),
                            Button(label="Voice", style=1, custom_id="VoiceChannel").to_dict(),
                            Button(
                                label="Link!",
                                style=5,
                                url=self.BASE_URL.format(bot_id=bot_id, permission=permission)
                            ).to_dict()
                        ]).to_dict())
                    elif custom_id == "VoiceChannel":
                        edited_message["components"].append(ActionRow([
                            Button(label="General", style=1, custom_id="General").to_dict(),
                            Button(label="Text", style=1, custom_id="TextChannel").to_dict(),
                            Button(label="Voice", style=1, custom_id="VoiceChannel", disabled=True).to_dict(),
                            Button(
                                label="Link!",
                                style=5,
                                url=self.BASE_URL.format(bot_id=bot_id, permission=permission)
                            ).to_dict()
                        ]).to_dict())

                    embed.add_field(
                        name="Permitted permissions",
                        value=get_permission_value(permission, option),
                        inline=True
                    )
                    edited_message["embed"] = embed.to_dict()
                    await self.bot.http.request(edit_route, json=edited_message)
                    return
                elif data.get("component_type") == 3:
                    values = data.get("values", [])
                    custom_id = data.get("custom_id")
                    values_hex = [int(i, 16) for i in values]

                    link_button: Button = components[1].components[3]
                    bot_id, permission = check_url(link_button.url)

                    for i in option.get(custom_id):
                        value = int(i.get("value"), 16)
                        if value & permission:
                            permission -= value

                    for i in values_hex:
                        permission += i

                    edited_message["components"].append(components[0].to_all_dict())

                    buttons: list = [i.to_dict() for i in components[1].components[0:3]]
                    buttons.append(
                        Button(
                            label="Link!",
                            style=5,
                            url=self.BASE_URL.format(bot_id=bot_id, permission=permission)
                        ).to_dict()
                    )

                    edited_message["components"].append(ActionRow(buttons).to_dict())
                    embed.add_field(
                        name="Permitted permissions",
                        value=get_permission_value(permission, option),
                        inline=True
                    )
                    edited_message["embed"] = embed.to_dict()
                    await self.bot.http.request(edit_route, json=edited_message)
                    return


def setup(client):
    client.add_cog(Socket(client))
