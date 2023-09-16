import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from app.help.const import CommandName, CommandNameList
from app.help.embed import get_help_embed
from components.ui.common.select import Select, SelectOption, SelectOptions
from components.ui.send import ViewSender
from components.ui.state import State
from components.ui.view import View, ViewObject

if TYPE_CHECKING:
    # import some original class
    from app.bot import Bot

    pass


class Help(commands.Cog):
    def __init__(self, bot: "Bot") -> None:
        self.bot = bot

    @app_commands.guilds(int(os.environ["GUILD_ID"]))  # type: ignore[arg-type]
    @app_commands.rename(command_name="コマンド名")
    @app_commands.command(name="help")
    async def send_help_command(self, interaction: discord.Interaction, command_name: CommandName | None = None) -> None:
        await interaction.response.defer(ephemeral=True)
        if not command_name:
            command_name = "help"
        view = ViewSender(HelpView(command_name=command_name))
        await view.send(interaction.followup)


class HelpView(View):
    def __init__(self, command_name: CommandName = "help") -> None:
        super().__init__()
        self.current: State[CommandName] = State(command_name, self)

    def export(self) -> ViewObject:
        async def on_select(interaction: discord.Interaction, values: list[str]) -> None:
            await interaction.response.defer(ephemeral=True)
            if (selected := values[0]) not in CommandNameList:
                selected = "help"
            self.current.set_state(selected)

        return ViewObject(
            embeds=[
                get_help_embed(self.current()),
            ],
            children=[
                Select(
                    options=SelectOptions(
                        max_values=1,
                        options=[
                            SelectOption(label=f"/{n}", value=n, selected_by_default=n == self.current())
                            for n in CommandNameList
                        ],
                    ),
                    style={
                        "placeholder": "使い方を見たいコマンドを選択してください。",
                    },
                    on_select=on_select,
                ),
            ],
        )


async def setup(bot: "Bot") -> None:
    await bot.add_cog(Help(bot))
