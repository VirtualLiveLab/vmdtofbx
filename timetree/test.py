import asyncio

from timetree import Client


async def main():
    client = Client()
    events = await client.get_upcoming_events()
    [print(event) for event in events]
    return


if __name__ == "__main__":
    asyncio.run(main())
