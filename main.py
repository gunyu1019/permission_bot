import os
from discord.ext import commands

from config.log_config import log
from config.config import parser

if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    prefix = parser.get("DEFAULT", "prefix")

    log.info("봇을 활성화 하고 있습니다.")
    if parser.getboolean("DEFAULT", "AutoShard"):
        log.info("Config 파일에서 AutoShard가 켜져있습니다. AutoShard 기능을 킵니다.")
        bot = commands.AutoShardedBot(command_prefix=prefix)
    else:
        bot = commands.Bot(command_prefix=prefix)

    cogs = ["cogs." + file[:-3] for file in os.listdir(os.path.join(directory, "cogs")) if file.endswith(".py")]
    for cog in cogs:
        bot.load_extension(cog)

    token = parser.get("DEFAULT", "token")
    bot.run(token)
