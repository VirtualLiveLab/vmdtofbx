import discord
from discord import Embed

from const.enums import Color
from utils.time import TimeUtils


def user_embed(
    user: discord.Member | discord.User,
) -> Embed:
    embed = Embed(
        title=user.display_name,
        color=Color.MIKU,
    )
    embed.add_field(
        name="Created at",
        value=TimeUtils.dt_to_str(user.created_at),
    )
    embed.add_field(
        name="ID",
        value=user.id,
    )
    embed.set_thumbnail(url=user.display_avatar.url)
    return embed
