import asyncio
import struct

from bleak import BleakClient, BleakScanner

from ..data import database
from ..data.models import DataStorage


class SitBluetooth:
    client: BleakClient = None

    def __init__(
        self,
        device: str = "DWM3001 Blue",
    ) -> None:
        self._deviceName = device
        self._isConnected = False
        self._connected_device = None

    async def manager(self, test_id):
        print("Starting connection manager.")
        self._test_id = test_id
        while True:
            if self.client:
                await self.connectDevice()
            else:
                await self.searchDevice()
                await asyncio.sleep(15.0)

    async def searchDevice(self):
        _scanner = BleakScanner()
        devices = await _scanner.discover(timeout=10.0)

        for device in devices:
            if device.name == self._deviceName:
                print("{}: {}".format(device.name, device.address))
                print("UUIDs: {}".format(device.metadata["uuids"]))
                self._connected_device = device
                self.client = BleakClient(
                    self._connected_device.address, self.on_disconnect
                )

    async def connectDevice(self):
        if self._isConnected:
            return
        try:
            await self.client.connect()
            self._isConnected = self.client.is_connected()
            if self._isConnected:
                print(f"Connected to {self._connected_device.name}")
                for service in self.client.services:
                    print("Services: {}".format(service))
                    for char in service.characteristics:
                        print("Char: {}".format(char))
                await self.write_command()
                while True:
                    if not self._isConnected:
                        break
                    await asyncio.sleep(5.0)
        except Exception as e:
            print("Exeption: {}".format(e))
            self._connected_device = None
            self.client = None

    async def cleanup(self):
        if self._isConnected:
            await self.disconnectDevice()

    async def disconnectDevice(self):
        await self.client.disconnect()
        self._isConnected = False

    async def read_char(self):
        test = await self.client.read_gatt_char(
            "6ba1de6b-3ab6-4d77-9ea1-cb6422720001"
        )  # BAS Char UUID 00002a19-0000-1000-8000-00805f9b34fb
        print("TEST {}".format(int.from_bytes(test, byteorder="big")))

    async def write_command(self):
        data = 5
        await self.client.write_gatt_char(
            "6ba1de6b-3ab6-4d77-9ea1-cb6422720002", data.to_bytes(1, byteorder="big")
        )  # BAS Char UUID 00002a19-0000-1000-8000-00805f9b34fb
        print("Send to Periphal")

    async def getNotification(self):
        await self.client.start_notify(
            "6ba1de6b-3ab6-4d77-9ea1-cb6422720001", self.on_notification
        )

    async def on_notification(self, sender: int, data: bytearray):
        distance = struct.unpack("f", data)
        print("From Handle {} Distance: {}".format(sender, distance[0]))
        await self.save_distance(distance[0])

    async def save_distance(self, distance):
        await database.repository.add_data(
            DataStorage(test_id=self._test_id, distance=distance)
        )

    def on_disconnect(self, client: BleakClient):
        print(f"Disconnected from {self._connected_device.name}!")
        self._connected_device = None
        self._isConnected = False

    def isConnected(self):
        return self._isConnected

    def getDeviceName(self):
        return self._deviceName
