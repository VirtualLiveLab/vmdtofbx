import asyncio
import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from components.ui.common.button import Button
from components.ui.common.select import Select, SelectOption, SelectOptions
from components.ui.send import ViewSender
from components.ui.state import State
from components.ui.status import StatusUI
from components.ui.view import View, ViewObject
from const.enums import Color, Status

if TYPE_CHECKING:
    # import some original class
    from app.bot import Bot

    pass


class TestCog(commands.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot

    @app_commands.guilds(int(os.environ["GUILD_ID"]))  # type: ignore[arg-type]
    @app_commands.command(name="try-status", description="StatusUIのテストコマンド")
    async def try_status(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()

        ui = StatusUI(color=Color.MIKU)
        ui.add(key="STATUS_1", message="ステータス1")
        ui.add(key="STATUS_2", message="ステータス2")

        # msg = await interaction.followup.send(embed=status.to_embed(), wait=True)
        # status.set_message(msg)
        await ui.send(interaction.followup, ephemeral=False)
        ui.update(
            key="STATUS_1",
            status=Status.IN_PROGRESS,
            message="ステータス1を実行中",
        )
        await ui.sync()
        # await msg.edit(embed=status.to_embed())

        await asyncio.sleep(5)
        ui.update(key="STATUS_1", status=Status.SUCCESS, message="ステータス1を完了")
        ui.update(key="STATUS_2", status=Status.IN_PROGRESS, message="ステータス2を実行中")
        await ui.sync()

        await asyncio.sleep(5)
        ui.update(key="STATUS_2", status=Status.FAILED, message="ステータス2でエラーが発生")
        await ui.sync()

    @app_commands.guilds(int(os.environ["GUILD_ID"]))  # type: ignore[arg-type]
    @app_commands.command(name="try-state", description="Stateのテストコマンド")
    async def try_state(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        view = ViewSender(TestView())
        await view.send(target=interaction.followup, ephemeral=False)


class TestView(View):
    def __init__(self) -> None:
        self.count = State(0, self)
        self.selected: State[list[str]] = State([], self)
        super().__init__()

    def export(self) -> ViewObject:
        async def increment(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            self.count.set_state(lambda x: x + 1)

        async def decrement(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            self.count.set_state(lambda x: x - 1)

        async def reset(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            self.count.set_state(0)

        async def on_select(interaction: discord.Interaction, values: list[str]) -> None:
            await interaction.response.defer()
            self.selected.set_state(values)

        e = discord.Embed(
            title="Count",
            description=f"Count: {self.count.get_state()}",
        )
        e.add_field(name="Selected", value="\n".join(self.selected.get_state()))

        return ViewObject(
            embeds=[e],
            children=[
                Button("+1", style={"color": "green"}, on_click=increment),
                Button("-1", style={"color": "red"}, on_click=decrement),
                Button(
                    "Reset",
                    style={
                        "color": "blurple",
                        "emoji": "🔄",
                        "disabled": self.count.get_state() == 0,
                    },
                    on_click=reset,
                ),
                Select(
                    options=SelectOptions(
                        max_values=2,
                        options=[
                            SelectOption(label="A", description="Aです"),
                            SelectOption(label="B", description="Bです"),
                        ],
                    ),
                    style={
                        "placeholder": "Select",
                        "row": 2,
                    },
                    on_select=on_select,
                ),
            ],
        )


async def setup(bot: "Bot") -> None:
    await bot.add_cog(TestCog(bot))
