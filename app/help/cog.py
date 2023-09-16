import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from app.help.const import FEATURE_LABEL_LIST, FeatureLabel
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
    @app_commands.rename(feature_name="機能")
    @app_commands.command(name="help")
    async def send_help_command(
        self,
        interaction: discord.Interaction,
        feature_name: FeatureLabel | None = None,
    ) -> None:
        await interaction.response.defer(ephemeral=True)
        if not feature_name:
            feature_name = "ヘルプ"
        view = ViewSender(HelpView(command_name=feature_name))
        await view.send(interaction.followup)


class HelpView(View):
    def __init__(self, command_name: FeatureLabel) -> None:
        super().__init__()
        self.current: State[FeatureLabel] = State(command_name, self)

    def export(self) -> ViewObject:
        async def on_select(interaction: discord.Interaction, values: list[str]) -> None:
            await interaction.response.defer(ephemeral=True)
            if (selected := values[0]) not in FEATURE_LABEL_LIST:
                selected = "ヘルプ"
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
                            SelectOption(label=n, value=n, selected_by_default=n == self.current())
                            for n in FEATURE_LABEL_LIST
                        ],
                    ),
                    style={
                        "placeholder": "使い方を見たい機能を選択してください。",
                    },
                    on_select=on_select,
                ),
            ],
        )


async def setup(bot: "Bot") -> None:
    await bot.add_cog(Help(bot))
