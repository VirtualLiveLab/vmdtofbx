import os
from typing import TYPE_CHECKING

import discord
from discord.ext import commands, tasks

from timetree.components.timetree import today_event_embed
from timetree import Client
from utils.finder import Finder
from utils.time import TimeUtils

if TYPE_CHECKING:
    # import some original class
    from app.bot import Bot

    pass


class TimeTree(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot
        self.send_today_event.start()

    def cog_unload(self):
        self.send_today_event.cancel()

    @tasks.loop(seconds=60)
    async def send_today_event(self):
        if not TimeUtils.get_now_jst().strftime("%H:%M") == "08:39":
            return

        client = Client()
        events = await client.get_upcoming_events()
        embed = today_event_embed(
            events=events,
            title="今日の予定",
            events_count=len(events),
        )

        channel = await Finder(self.bot).find_channel(int(os.environ["CHANNEL_ID"]), type=discord.TextChannel)
        await channel.send(embed=embed)
        return


async def setup(bot: "Bot"):
    await bot.add_cog(TimeTree(bot))
