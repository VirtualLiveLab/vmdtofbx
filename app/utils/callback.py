from typing import Literal

import discord

from app.utils.embed import fix_embed, wip_embed


async def command_unavailable_callback(
    interaction: discord.Interaction,
    /,
    *,
    ephemeral: bool = False,
    status: Literal["FIX", "WIP"],
) -> None:
    e = wip_embed() if status == "WIP" else fix_embed()
    if interaction.response.is_done():
        await interaction.followup.send(embed=e, ephemeral=ephemeral)
        return

    await interaction.response.send_message(embed=e, ephemeral=ephemeral)
    return
