"""This is the main script"""
import asyncio
import time
from SitBluetooth import SitBluetooth

async def main():
    enable_notify = False
    while(1):
        if(device.isConnected() and not enable_notify):
            await device.getNotification()
            enable_notify = True

        await asyncio.sleep(1)

if __name__ == "__main__":
    # Create the event loop.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    device = SitBluetooth()
    try:
        #TODO ensure_future is deprecated find other solution
        asyncio.ensure_future(device.manager())
        asyncio.ensure_future(main())
        loop.run_forever()
    except KeyboardInterrupt:
        print()
        print("User stopped program.")
    finally:
        print("Disconnecting...")
        loop.run_until_complete(device.cleanup())