import threading
import asyncio
import time

class HandleSystemController:
    stationReset = False
    diagScanResults = True
    stationSendSetup = False
    stationSaveAll = False
    scEraseFlash = False
    scProgFlash = False

    def __init__(self, gui, station):
        self.station = station
        self.gui = gui
        mainThread = threading.Thread(
            target=asyncio.run, args=(self.mainTask(),), daemon=True
        )
        mainThread.start()
    
    async def mainTask(self):

        stat = 1
        # self.gui.showStation(7)
        while True:

            await self.scanTask()
            print("BLScan")
            time.sleep(1)
            
    async def scanTask(self):
        if self.stationReset:
            await self.station.resetStations()
            self.stationReset = False
        elif self.stationSendSetup:
            await self.station.sendStationSetup()
            self.stationSendSetup = False
        elif self.stationSaveAll:
            self.SaveSettings()
            self.stationSaveAll = False
        elif self.scEraseFlash:
            await self.station.sendEraseFlash()
            self.scEraseFlash = False
        elif self.scProgFlash:
            print("5")
            await self.station.serial.scProgramFlash()
            self.scProgFlash = False
        else:
            # await self.station.performScan()
            self.newScanDataAvail = True
