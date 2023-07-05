import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from const.enums import Role
from utils.validator import validate

if TYPE_CHECKING:
    # import some original class
    from app.bot import Bot

    pass


class Buhi(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    group = app_commands.Group(
        name="buhi",
        description="部費ロール管理",
        guild_ids=[int(os.environ["GUILD_ID"])],
    )

    @commands.Cog.listener("on_member_join")
    async def add_minou_role_automatically(self, member: discord.Member):
        await self.add_minou_role(member)
        return

    @group.command(
        name="add",
        description="部費未納ロールを付与します",
    )
    @app_commands.guild_only()
    async def add_minou_role_command(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer()
        author = validate(interaction.user, discord.Member)
        if not self.check_kaikei_role(author):
            await interaction.followup.send("権限がありません。")
            return

        await interaction.followup.send(f"{member.display_name}に部費未納ロールを付与しています...")

        try:
            await self.add_minou_role(member)
        except Exception as e:
            self.bot.logger.error(e)
            await interaction.followup.send(f"エラー: {member.display_name}に部費未納ロールを付与できませんでした。\n\n{e}")
        else:
            await interaction.followup.send(content=f"{member.display_name}に部費未納ロールを付与しました！")
        return

    @group.command(
        name="remove",
        description="部費未納ロールを消去します",
    )
    @app_commands.guild_only()
    async def remove_minou_role_command(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer()
        author = validate(interaction.user, discord.Member)
        if not self.check_kaikei_role(author):
            await interaction.followup.send("権限がありません。")
            return

        await interaction.followup.send(f"{member.display_name}から部費未納ロールを消去しています...")

        try:
            await self.remove_minou_role(member)
        except Exception as e:
            self.bot.logger.error(e)
            await interaction.followup.send(f"エラー: {member.display_name}から部費未納ロールを消去できませんでした。\n\n{e}")
        else:
            await interaction.followup.send(content=f"{member.display_name}から部費未納ロールを消去しました！")
        return

    async def add_minou_role(self, member: discord.Member):
        if Role.BUHI_MINOU in [r.id for r in member.roles]:
            return
        await member.add_roles(discord.Object(id=Role.BUHI_MINOU))
        return

    async def remove_minou_role(self, member: discord.Member):
        if Role.BUHI_MINOU not in [r.id for r in member.roles]:
            return
        await member.remove_roles(discord.Object(id=Role.BUHI_MINOU))
        return

    def check_kaikei_role(self, member: discord.Member):
        return Role.KAIKEI in [r.id for r in member.roles]


async def setup(bot: "Bot"):
    await bot.add_cog(Buhi(bot))
