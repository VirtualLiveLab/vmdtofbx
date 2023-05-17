from discord import Embed

from const.enums import Color


def ready_embed(
    latency: float,
    failed_exts: list[str],
    failed_views: list[str],
):
    embed = Embed(
        description="ミクが起動したよ!",
        color=Color.MIKU,
    )
    embed.add_field(
        name="latency",
        value=f"{latency * 1000:.2f}ms",
        inline=False,
    )
    if failed_exts:
        embed.add_field(
            name="拡張機能の読み込みに失敗したよ!",
            value="\n".join(failed_exts),
            inline=False,
        )
    if failed_views:
        embed.add_field(
            name="Viewの読み込みに失敗したよ!",
            value="\n".join(failed_views),
            inline=False,
        )
    return embed
