import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands, tasks

from app.timetree.components.timetree import today_event_embed
from const.enums import Color
from timetree import Client as TimeTreeClient
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
        embed = await self.get_timetree_embed()
        channel = await Finder(self.bot).find_channel(int(os.environ["CHANNEL_ID"]), type=discord.TextChannel)
        await channel.send(embed=embed)
        return

    @app_commands.guilds(int(os.environ["GUILD_ID"]))
    @app_commands.command(name="timetree")
    async def send_timetree(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=False)
        embed = await self.get_timetree_embed()
        await interaction.followup.send(embed=embed)
        return

    async def get_timetree_embed(self):
        client = TimeTreeClient()
        try:
            events = await client.get_upcoming_events()
        except Exception as e:
            self.bot.logger.error(e)
            return discord.Embed(
                title="TimeTreeからの情報取得に失敗しました",
                description="時間をおいてもう一度お試しください",
                color=Color.WARNING,
            )
        else:
            return today_event_embed(
                events=events,
                title="今日の予定",
                events_count=len(events),
            )


async def setup(bot: "Bot"):
    await bot.add_cog(TimeTree(bot))
