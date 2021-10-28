import asyncio
from bleak import BleakClient, discover

class SitBluetooth:

    client: BleakClient = None

    def __init__(
        self, 
        loop: asyncio.AbstractEventLoop,
        device: str ="DWM1001",
    ) -> None:
        self._deviceName = device
        self.loop = loop
        self._isConnected = False
        self._connected_device = None

    async def manager(self):
        print("Starting connection manager.")
        while True:
            if self.client:
                await self.connectDevice()
            else:
                await self.searchDevice()
                await asyncio.sleep(15.0, loop=self.loop)  

    async def searchDevice(self):
        devices = await discover()
        
        for device in devices:
            if device.name == self._deviceName:
                print("{}: {}".format(device.name, device.address))
                print("UUIDs: {}".format(device.metadata["uuids"]))
                print("RSSI: {}".format(device.rssi))
                self._connected_device = device
                self.client = BleakClient(self._connected_device.address, loop=self.loop)

    async def connectDevice(self):
        if self._isConnected:
            return
        try:
            await self.client.connect()
            self._isConnected = await self.client.is_connected()
            if self._isConnected:
                print(f"Connected to {self._connected_device.name}")
                self.client.set_disconnected_callback(self.on_disconnect)
                while True:
                    if not self._isConnected:
                        break
                    await asyncio.sleep(5.0, loop=self.loop)
        except Exception as e:
            print("Exeption: {}".format(e))

    def on_disconnect(self, client: BleakClient):
        self._isConnected = False
        self.client = None
        # Put code here to handle what happens on disconnet.
        print(f"Disconnected from {self._connected_device.name}!")
        self._connected_device = None

    async def cleanup(self):
        await self.disconnectDevice()

    def isConnected(self):
        return self._isConnected

    async def disconnectDevice(self):
        await self.client.disconnect()
        self._isConnected = False

    def getDeviceName(self):
        return self._deviceName