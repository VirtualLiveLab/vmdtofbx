from discord import Embed

from app.help.const import CommandName
from const.enums import Color


def get_help_embed(name: CommandName) -> Embed:
    d: dict[CommandName, Embed] = {
        "buhi": buhi_embed(),
        "help": help_embed(),
        "helloworld": helloworld_embed(),
        "miku": miku_embed(),
        "vote": vote_embed(),
        "timetree": timetree_embed(),
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


def helloworld_embed() -> Embed:
    e = _base_embed()
    e.title = "`/helloworld`"
    e.description = "Hello World!を表示します。"
    return e


def miku_embed() -> Embed:
    e = _base_embed()
    e.title = "`/miku`"
    e.description = "ミクさんが返事をしてくれるよ！"
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
リアクションを使って投票し、集計するときはそのメッセージを右クリック(PC) or 長押し(スマホ)して、
「投票を集計」を選択してください。
""",
        inline=False,
    )
    return e


def timetree_embed() -> Embed:
    e = _base_embed()
    e.title = "`/timetree`(非推奨)"
    e.description = "TimeTreeのAPIを使って今日の予定を表示します。"
    e.add_field(
        name=":warning:",
        value="""
この機能は2023年12月22日以降使用できなくなります。
理由は[TimeTreeのAPIが廃止されるため](https://timetreeapp.com/intl/ja/newsroom/2023-07-23/connectapp-api)です。
ご迷惑をおかけします。
""",
        inline=False,
    )
    return e
