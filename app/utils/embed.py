from discord import Embed

from const.enums import Color


def wip_embed() -> Embed:
    return Embed(title="準備中", description="この機能は現在準備中です。もうちょっとまってね！", color=Color.MIKU)


def fix_embed() -> Embed:
    return Embed(title="修正中", description="この機能は現在修正中です。もうちょっとまってね！", color=Color.MIKU)
