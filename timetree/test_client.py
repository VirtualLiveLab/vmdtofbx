import asyncio
import os
from logging import getLogger

from dotenv import load_dotenv

from timetree.client import Client


async def main() -> None:
    logger = getLogger(__name__)
    api_key = os.getenv("API_KEY", "")
    calendar_id = os.getenv("CALENDAR_ID", "")
    client = Client(api_key, calendar_id=calendar_id)
    events = await client.get_upcoming_events(days=7)
    for e in events:
        logger.debug(e)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
