"""This is the main script"""
import asyncio
import time
from SitBluetooth import SitBluetooth

async def main():
    while(1):
        if device.isConnected():
            print("Test")
        await asyncio.sleep(1)

if __name__ == "__main__":
    # Create the event loop.
    loop = asyncio.get_event_loop()

    device = SitBluetooth(loop)
    try:
        asyncio.ensure_future(device.manager())
        asyncio.ensure_future(main())
        loop.run_forever()
    except KeyboardInterrupt:
        print()
        print("User stopped program.")
    finally:
        print("Disconnecting...")
        loop.run_until_complete(device.cleanup())