import os

from app.bot import Bot

if __name__ == "__main__":
    bot = Bot()
    bot.runner(token=os.environ["DISCORD_BOT_TOKEN"])
