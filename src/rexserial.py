import serial
import time
import asyncio
from commands import SysControlCommands


# Configure the serial port
port = "/dev/ttyS1"  # Serial Port Number
baudrate = 115200  # Baud rate
timeout = 1  # Timeout in seconds for read operations


class serialPolling:
    scprogramstruct = 0
    scProgFlashResponse = False
    firstLine = False

    def __init__(self, port, baud, timeout):
        # Open serial port
        try:
            self.ser = serial.Serial(
                port=port, bytesize=serial.EIGHTBITS, baudrate=baud, timeout=timeout
            )
            self.running = True
        except serial.SerialException as e:
            # Send message to GUI
            self.errorcode = e

    async def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    # |Header|Length|Command|NodeID|Data|0x00|
    async def pollReadController(self):
        # Transmit
        if self.running:
            if self.ser and self.ser.in_waiting > 0:
                data = self.ser.read(self.ser.in_waiting)
                return data

    async def pollWriteController(self, data):
        if self.ser:
            self.ser.write(data)

    # COBS encode
    def PktEncode(self, data: bytes):

        length = len(data)
        encoded = bytearray()

        block_start = 0
        while block_start < length:
            block_end = block_start
            while block_end < length and data[block_end] != 0:
                block_end += 1

            block_size = block_end - block_start + 1
            encoded.append(block_size)
            encoded.extend(data[block_start:block_end])
            block_start = block_end + 1

        encoded.append(0)

        return bytes(encoded)

    # COBS decode
    def PktDecode(self, data: bytes) -> bytes:
        length = len(data)
        decoded = bytearray()

        block_start = 0
        while block_start < length:
            block_size = data[block_start]
            if block_size == 0:
                break

            block_end = block_start + block_size
            decoded.extend(data[block_start + 1 : block_end])

            if block_size < 0xFF:
                decoded.append(0)

            block_start = block_end

        return bytes(decoded)

    async def scProgramFlash(self):
        count = self.scprogramstruct["byte_count"]
        address = self.scprogramstruct["address"]
        data = self.scprogramstruct["data"]
        cmd = []
        response = []
        
        # 0xAF|Cnt+7|0x14(cmd)|Add0|Add1|Add2|Add3|Data
        adr = 0xA0 | 0x0F
        cmd.append(SysControlCommands.RECEIVESCAPP.value)
        cmd.insert(0,adr)
        cmd.insert(1, 7+count)
        intval16 = address.to_bytes(4, 'little')
        if self.firstLine:
            self.firstLine = False
            cmd.insert(2,0x21)
        else:
            cmd.insert(2,0x20)
        cmd.insert(3,intval16[0])
        cmd.insert(4,intval16[1])
        cmd.insert(5,intval16[2])
        cmd.insert(6,intval16[3])
        for each_value in bytes(data):
            cmd.append(each_value)
        programDataPkt = self.PktEncode(cmd)
        pkt = bytes(programDataPkt)
        print("pkt=", bytes(pkt))
        # Send packet
        await self.pollWriteController(pkt)
        time.sleep(0.05)
        response = await self.pollReadController()
        print("Response=",response)
        if response is not None:
            self.scProgFlashResponse = True
            dcdpkt = self.PktDecode(response)
        else:
            dcdpkt = 1

        return dcdpkt

    async def Poll(self, node, command):
        cmd = []
        response = []
        address = 0xA0 | node
        cmd.append(command)
        cmd.insert(0, address)
        cmd.insert(1, 3)  # Length = 3
        value = bytes(cmd)
        requestStatusPkt = self.PktEncode(value)
        # Send packet
        await self.pollWriteController(requestStatusPkt)
        time.sleep(0.05)
        response = await self.pollReadController()
        dcdpkt = self.PktDecode(response)

        return dcdpkt

    async def SendCmd(self, node, command, data):
        # Address, Length, Cmd, <Data>
        cmd = []
        response = []
        address = 0xA0 | node
        cmd.append(command)
        cmd.insert(0, address)
        cmd.insert(1, 10)  # Length = 10
        for i in range(7):
            cmd.append(int(data[i]))
        value = bytes(cmd)
        requestStatusPkt = self.PktEncode(value)
        # Send packet
        await self.pollWriteController(requestStatusPkt)
        time.sleep(0.05)
        response = await self.pollReadController()
        dcdpkt = self.PktDecode(response)

        return dcdpkt


def call_prog_flash():
    """A synchronous function that calls an async function."""
    asyncio.run(stest.scProgramFlash())

if __name__ == "__main__":
    stest = serialPolling("/dev/ttyS1", 115200, 1)
    stest.scprogramstruct = {"byte_count": 10,
                    "address": 134348800,
                    "record_type": 0,
                    "data": [0,1,2,3,65,70,6,7],
                    "checksum": 0x70,}
    call_prog_flash()