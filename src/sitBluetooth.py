"""This is the main script"""
import asyncio
import time

from .bluetooth.bluetooth import SitBluetooth
from .config.settings import settings
from .data import database
from .data.models import Test


device = SitBluetooth()


async def main():
    enable_notify = False
    while 1:
        if device.isConnected() and not enable_notify:
            await device.getNotification()
            enable_notify = True

        await asyncio.sleep(1)


async def db_test_init():
    print("Please insert Test Name: ")
    string = str(input())
    test = await database.repository.add_test(Test(name=string))
    return test.id


def start():
    print(settings.database_url)
    database.create_db_and_tables()

    # Create the event loop.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    test_id = loop.run_until_complete(db_test_init())
    try:
        # TODO ensure_future is deprecated find other solution
        asyncio.ensure_future(device.manager(test_id))
        asyncio.ensure_future(main())
        loop.run_forever()
    except KeyboardInterrupt:
        print()
        print("User stopped program.")
    finally:
        print("Disconnecting...")
        loop.run_until_complete(device.cleanup())
