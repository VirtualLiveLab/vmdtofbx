import os
from typing import TypeVar, overload

import discord
from discord import Thread
from discord.abc import GuildChannel, PrivateChannel

from .const import literal
from .logger import get_my_logger
from .validator import validate

T = TypeVar("T", bound=GuildChannel | PrivateChannel | Thread)


class Finder:
    def __init__(self, bot: discord.Client) -> None:
        self.bot = bot
        self.logger = get_my_logger("Finder")

    @overload
    async def find_channel(
        self,
        channel_id: int,
        expected_type: None = None,
    ) -> GuildChannel | PrivateChannel | Thread:
        ...

    @overload
    async def find_channel(self, channel_id: int, expected_type: type[T]) -> T:
        ...

    async def find_channel(
        self,
        channel_id: int,
        expected_type: type[T] | None = None,
    ) -> GuildChannel | PrivateChannel | Thread:
        channel = self.bot.get_channel(channel_id)
        if not channel:
            try:
                channel = await self.bot.fetch_channel(channel_id)
            except Exception as e:
                self.logger.exception(literal.CHANNEL_NOT_FOUND, exc_info=e)
                raise

        if not expected_type:
            return channel

        return validate(channel, expected_type)

        # if isinstance(type, list):
        #     for t in type:
        #         if isinstance(channel, t):
        #             return channel
        # else:
        #     if not isinstance(channel, type):
        #         self.logger.exception(literal.CHANNEL_NOT_FOUND)
        #         raise TypeError(f"Channel is not a {type}")
        # return channel

    async def find_log_channel(self) -> discord.TextChannel:
        return await self.find_channel(int(os.environ["LOG_CHANNEL_ID"]), expected_type=discord.TextChannel)

    async def find_guild(self, guild_id: int) -> discord.Guild:
        guild = self.bot.get_guild(guild_id)
        if not guild:
            try:
                guild = await self.bot.fetch_guild(guild_id)
            except Exception as e:
                self.logger.exception(literal.CHANNEL_NOT_FOUND, exc_info=e)
                raise
        return guild

    async def find_role(self, guild_id: int, role_id: int) -> discord.Role:
        guild = await self.find_guild(guild_id)
        role = guild.get_role(role_id)
        if not role:
            roles = await guild.fetch_roles()
            role = next(r for r in roles if r.id == role_id)
            if not role:
                self.logger.exception(literal.CHANNEL_NOT_FOUND)
                raise
        return role

    async def find_member(self, guild_id: int, user_id: int) -> discord.Member | None:
        member: discord.Member | None = None
        guild = await self.find_guild(guild_id)
        member = guild.get_member(user_id)
        if not member:
            try:
                member = await guild.fetch_member(user_id)
            except Exception as e:
                self.logger.exception(literal.USER_NOT_FOUND, exc_info=e)
                member = None
        return member

    async def find_user(self, user_id: int) -> discord.User | None:
        user: discord.User | None = None
        user = self.bot.get_user(user_id)
        if user:
            return user

        try:
            user = await self.bot.fetch_user(user_id)
        except Exception as e:
            self.logger.exception(literal.USER_NOT_FOUND, exc_info=e)
            user = None
        return user

    # @staticmethod
    # def find_bot_permissions(
    #     guild: discord.Guild,
    #     place: discord.abc.GuildChannel | discord.Thread,
    # ) -> discord.Permissions:
    #     role = guild.get_role(int(os.environ["BOT_ROLE"]))
    #     if not role:
    #         msg = "BOT_ROLE is not set"
    #         raise Exception(msg)

    #     perms: discord.Permissions = place.permissions_for(role)
    #     return perms
