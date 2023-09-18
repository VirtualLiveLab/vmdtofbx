from discord import Embed

from app.help.const import FeatureLabel
from const.enums import Color


def get_help_embed(name: FeatureLabel) -> Embed:
    d: dict[FeatureLabel, Embed] = {
        "部費ロール": buhi_embed(),
        "ヘルプ": help_embed(),
        "その他": other_embed(),
        "投票": vote_embed(),
        "ピン留め": pin_embed(),
        "メッセージ展開": dispand_embed(),
    }
    return d[name]


def _base_embed() -> Embed:
    return Embed(color=Color.MIKU)


def buhi_embed() -> Embed:
    return _base_embed()


def help_embed() -> Embed:
    e = _base_embed()
    e.title = "`/help`"
    e.description = "コマンドの使い方(これ)を表示します。"
    return e


def other_embed() -> Embed:
    e = _base_embed()
    e.title = "その他の機能"
    e.add_field(
        name="`/helloworld`",
        value="Hello World!を表示します。",
    )
    e.add_field(
        name="`/miku`",
        value="ミクさんが返事をしてくれるよ！",
    )
    return e


def vote_embed() -> Embed:
    e = _base_embed()
    e.title = "`/vote`"
    e.description = "投票を作成します。"
    e.add_field(
        name="使い方(2択)",
        value="""
質問文のみを指定すると自動的に2択の投票が作成されます。
例: `/vote 今日の晩御飯は？`
""",
        inline=False,
    )
    e.add_field(
        name="使い方(3択以上)",
        value="""
質問文を入力したあと、続けて選択肢を入力してください。
最大で20個まで入力できます。
例: `/vote 今日の晩御飯は？ ラーメン うどん そば`
""",
        inline=False,
    )
    e.add_field(
        name="使い方(集計)",
        value="""
`/vote`コマンドを実行すると、投票の詳細とリアクションがついたメッセージが送信されます。
集計するときはそのメッセージを右クリック(PC) or 長押し(スマホ)して、
「投票を集計」を選択してください。
""",
        inline=False,
    )
    return e


def pin_embed() -> Embed:
    e = _base_embed()
    e.title = "ピン留め"
    e.description = "メッセージをピン留め(もしくは解除)します。"
    e.add_field(
        name="使い方",
        value="""
メッセージを右クリック(PC) or 長押し(スマホ)して、
「Pin / Unpin」を選択してください。

まだピン留めされていないメッセージを選択するとピン留めされ、
ピン留めされたメッセージを選択するとピン留めが解除されます。
""",
        inline=False,
    )
    return e


def dispand_embed() -> Embed:
    e = _base_embed()
    e.title = "メッセージ展開"
    e.description = "メッセージURLを展開します。"
    e.add_field(
        name="使い方",
        value="Mikubotが導入されているかつ__**閲覧権限がある**__チャンネルのメッセージURLを送信すると、埋め込みで展開されます。",
        inline=False,
    )
    return e
