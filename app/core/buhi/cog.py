import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from components.embed.status import StatusEmbed
from const.enums import Color, Role
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

    # TODO DiscordのOnboarding機能に移行しない場合コメントアウトを外す
    # @commands.Cog.listener("on_member_join")
    # async def add_minou_role_automatically(self, member: discord.Member):
    #     await self.add_minou_role(member)
    #     return

    @group.command(
        name="add",
        description="部費未納ロールを付与します",
    )
    @app_commands.guild_only()
    async def add_minou_role_command(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer()
        author = validate(interaction.user, discord.Member)
        status = StatusEmbed(
            default_label=f"{member.mention}に部費未納ロールを付与しています...",
            color=Color.MIKU,
        )
        if not self.check_kaikei_role(author):
            embed = status.fail(
                label="このコマンドを実行する権限がありません。",
                color=Color.WARNING,
            )
            await interaction.followup.send(embed=embed)
            return

        msg = await interaction.followup.send(embed=status.loading(), wait=True)

        try:
            await self.add_minou_role(member)
        except Exception as e:
            self.bot.logger.error(e)
            embed = status.fail(
                label=f"{member.mention}に部費未納ロールを付与できませんでした。",
                color=Color.WARNING,
            )
            embed.add_field(
                name="エラー内容",
                value=f"```\n{e}\n```",
            )
            await msg.edit(embed=embed)
        else:
            embed = status.success(
                label=f"{member.mention}に部費未納ロールを付与しました！",
                color=Color.SUCCESS,
            )
            await msg.edit(embed=embed)
        return

    @group.command(
        name="remove",
        description="部費未納ロールを消去します",
    )
    @app_commands.guild_only()
    async def remove_minou_role_command(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer()
        author = validate(interaction.user, discord.Member)
        status = StatusEmbed(
            default_label=f"{member.mention}から部費未納ロールを消去しています...",
            color=Color.MIKU,
        )
        if not self.check_kaikei_role(author):
            embed = status.fail(
                label="このコマンドを実行する権限がありません。",
                color=Color.WARNING,
            )
            await interaction.followup.send(embed=embed)
            return

        msg = await interaction.followup.send(embed=status.loading(), wait=True)

        try:
            await self.remove_minou_role(member)
        except Exception as e:
            self.bot.logger.error(e)
            embed = status.fail(
                label=f"{member.mention}から部費未納ロールを消去できませんでした。",
                color=Color.WARNING,
            )
            embed.add_field(
                name="エラー内容",
                value=f"```\n{e}\n```",
            )
            await msg.edit(embed=embed)
        else:
            embed = status.success(
                label=f"{member.mention}から部費未納ロールを消去しました！",
                color=Color.SUCCESS,
            )
            await msg.edit(embed=embed)
        return

    async def add_minou_role(self, member: discord.Member):
        if Role.BUHI_MINOU in [r.id for r in member.roles]:
            raise Exception(f"{member.mention}には既に部費未納ロールが付与されています。")
        await member.add_roles(discord.Object(id=Role.BUHI_MINOU))
        return

    async def remove_minou_role(self, member: discord.Member):
        if Role.BUHI_MINOU not in [r.id for r in member.roles]:
            raise Exception(f"{member.mention}には部費未納ロールが付与されていません。")
        await member.remove_roles(discord.Object(id=Role.BUHI_MINOU))
        return

    def check_kaikei_role(self, member: discord.Member):
        return Role.KAIKEI in [r.id for r in member.roles]


async def setup(bot: "Bot"):
    await bot.add_cog(Buhi(bot))
