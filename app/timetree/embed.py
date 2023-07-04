import datetime

from discord import Embed

from const.enums import Color
from timetree import Event


def today_event_embed(
    events: list[Event],
    title: str,
    events_count: int,
) -> Embed:
    # Embed field limit:25
    # if over 25, add caution description and link to timetree
    too_many_events = False
    if len(events) > 25:
        events = events[:25]
        too_many_events = True

    description = "{month}月{day}日の予定は{events_count}件だよ!\n\n".format(
        month=datetime.date.today().month,
        day=datetime.date.today().day,
        events_count=events_count,
    )
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
                url=f"\n[TimeTreeで見る]({str(event.url)})" if event.url else "",
            ),
            inline=False,
        )

    return embed
