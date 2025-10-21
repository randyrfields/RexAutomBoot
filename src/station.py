import tkinter as tk
import struct
from rexserial import serialPolling
from enum import Enum


class SysControlCommands(Enum):
    NOP = 0
    GETSTATUS = 1
    RESETSTATIONS = 15
    SCANRESULTS = 16
    CALIBRATESTATIONS = 17
    STATIONORDER = 18
    RECEIVESCAPP = 20
    EXITBOOTLOADER = 22
    ERASEFLASH = 23
    SENDSCPROGRAMDATA = 24
    SENDTFPROGRAMDATA = 25


class Station:

    nodeStatus = []

    def __init__(self, mainWindow):

        self.mainWindow = mainWindow
        self.totalNumberStations = 0
        self.serial = serialPolling("/dev/ttyS1", 115200, 1)

        # Create list for status storage
        for i in range(0, 8):
            row = []
            for j in range(48):
                row.append(0)
            self.nodeStatus.append(row)

    async def performScan(self):
        rawData = []
        for x in range(1, 8):
            cmd = SysControlCommands.GETSTATUS

            try:
                result = await self.serial.Poll(x, cmd.value)
                print("Scan")
            except:
                result = bytes([0xA7, 0x29, 0x01, 0x05, 0x00]) + bytes([0x00] * 32)


    async def sendStationOrder(self):

        cmd = SysControlCommands.STATIONCONFIG

        try:
            node = 0x0F
            data = self.mainWindow.stationOrderList.get()
            result = await self.serial.SendCmd(node, cmd.value, data)
        except:
            result = bytes([0xFF, 0xFF, 0xFF, 0xFF])

        if result[3] == 0xAC:
            self.mainWindow.terminal.addTextTerminal("System function reset success.\n")
        else:
            # print Failed message
            self.mainWindow.terminal.addTextTerminal("System function reset fail.\n")


    async def sendEraseFlash(self):
        cmd = SysControlCommands.ERASEFLASH
        
        try:
            node = 0x0F
            result = await self.serial.Poll(node, cmd.value)
        except:
            result = bytes([0xFF, 0xFF, 0xFF, 0xFF])

        return result


    async def sendSCProgramData(self):
        cmd = SysControlCommands.SENDSCPROGRAMDATA

        try:
            node = 0x0F
            result = await self.serial.Poll(node, cmd.value)
        except:
            result = bytes([0xFF, 0xFF, 0xFF, 0xFF])

        return result
