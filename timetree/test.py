import asyncio

from timetree.client import Client

if not __debug__:
    from dotenv import load_dotenv

    load_dotenv()


async def main():
    client = Client()
    events = await client.get_upcoming_events()
    [print(event) for event in events]
    return


if __name__ == "__main__":
    asyncio.run(main())
