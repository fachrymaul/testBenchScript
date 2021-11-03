from typing import ByteString
import serial
from crc import crc16

class EDMI_TestBench:
    def __init__(self, serialInstance=None):
        self.serial = serialInstance
        self.len = 0
        self.command = 0
        self.data = bytearray()
        self.txBuffer = bytearray()
        self.rxBuffer = bytearray()
        self.soi = 0x7E
        self.eoi = 0xFF
        self.crc = 0

    def __appendSOIToTxBuffer(self):
        self.txBuffer.append(self.soi)
    
    def __appendLenToTxBuffer(self):
        self.txBuffer.append(self.len & 0xFF)
        self.txBuffer.append((self.len >> 8) & 0xFF)
        self.txBuffer.append((self.len >> 16) & 0xFF)
        self.txBuffer.append((self.len >> 32) & 0xFF)

    def __appendCommandToTxBuffer(self):
        self.txBuffer.append((self.command >> 8) & 0xFF)
        self.txBuffer.append(self.command & 0xFF)

    def __appendDataToTxBuffer(self):
        if self.data is not None:
            self.txBuffer.extend(self.data)
    
    def __calculateCRC(self):
        data = bytearray()
        data.append((self.command >> 8) & 0xFF)
        data.append(self.command & 0xFF)
        if len(self.data) > 0:
            data.extend(self.data)
        print(data)
        
        self.crc = crc16(data)

    def __appendCRCToTxBuffer(self):
        self.txBuffer.append((self.crc >> 8) & 0xFF)
        self.txBuffer.append(self.crc & 0xFF)
    
    def __appendEOIToTxBuffer(self):
        self.txBuffer.append(self.eoi)

    def printTxBufferInHex(self):
        print(self.txBuffer)
    
    def __clearTxBuffer(self):
        self.txBuffer = bytearray()
    
    def __calculateLength(self):
        self.len = 2 + len(self.data)

    def __constructMessage(self):
        self.__clearTxBuffer()
        self.__appendSOIToTxBuffer()
        self.__calculateLength()
        self.__appendLenToTxBuffer()
        self.__appendCommandToTxBuffer()
        self.__appendDataToTxBuffer()
        self.__calculateCRC()
        self.__appendCRCToTxBuffer()
        self.__appendEOIToTxBuffer()
    
    def sendMessage(self):
        self.serial.write(self.txBuffer)
    
    def commandOnline(self):
        self.data = bytearray()
        self.command = 0x8000
        self.__constructMessage()

    def commandOffline(self):
        self.data = bytearray()
        self.command = 0x8100
        self.__constructMessage()

    def commandAdjustSpeed(self):
        self.data = bytearray()
        self.command = 0x8200
        self.data.append(0x01)
        self.__constructMessage()


        

print("hello world")
comPort = serial.Serial("COM12")

if comPort.is_open is True:
    comPort.close()
comPort.open()


temp = EDMI_TestBench(comPort)
temp.commandOnline()
temp.printTxBufferInHex()
temp.sendMessage()

