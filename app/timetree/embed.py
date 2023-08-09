import datetime

from discord import Embed

from const.enums import Color
from timetree import Event
from utils.time import JST

# Embed field limit:25
# if over 25, add caution description and link to timetree
MAX_EMBED_FIELD = 25


def today_event_embed(
    events: list[Event],
    title: str,
    events_count: int,
) -> Embed:
    # Embed field limit:25
    # if over 25, add caution description and link to timetree
    too_many_events = False
    if len(events) > MAX_EMBED_FIELD:
        events = events[:MAX_EMBED_FIELD]
        too_many_events = True

    today = datetime.datetime.now(tz=JST()).date()
    description = f"{today.month}月{today.day}日の予定は{events_count}件だよ!\n\n"
    if too_many_events:
        description += "\N{Warning Sign} 26件以上の予定があるよ! 26件目以降はTimeTreeを確認してね!\n"

    embed = Embed(
        title=title,
        description=description,
        color=Color.MIKU,
    )
    for event in events:
        embed.add_field(
            name=event.title,
            value="終日"
            if event.all_day
            else "{start} ~ {end}{url}".format(
                start=event.start_at.strftime("%H:%M"),
                end=event.end_at.strftime("%H:%M"),
                url=f"\n[TimeTreeで見る]({event.url!s})" if event.url else "",
            ),
            inline=False,
        )

    return embed
