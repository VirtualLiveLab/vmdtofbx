from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, HttpUrl


class Event(BaseModel):
    event_id: str
    event_type: Literal["event"]

    # attributes
    category: Literal["schedule", "keep"]
    title: str
    all_day: bool
    start_at: datetime  # "2019-03-18T09:53:33.123Z"
    start_timezone: str
    end_at: datetime  # "2019-03-18T09:53:33.123Z"
    end_timezone: str
    recurrence: list[str] | None = [""]
    description: str | None = ""
    location: str
    url: HttpUrl | None
    updated_at: datetime  # "2019-03-18T09:53:33.123Z"
    created_at: datetime  # "2019-03-18T09:53:33.123Z"

    raw_data: dict[str, Any]
