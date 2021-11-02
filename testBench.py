import serial
import crcmod

class EDMI_TestBench:
    def __init__(self, port=None, serialInstance=None):
        self.serial = serialInstance
        self.port = port
        self.len = 0
        self.command = 0
        self.data = None
        self.txBuffer = None
        self.rxBuffer = None
        self.soi = 0x7E
        self.eoi = 0xFF

    def appendSOIToTxBuffer(self):
        self.txBuffer.append(self.soi)
    
    def appendLenToTxBuffer(self):
        self.txBuffer.append(self.len)

    def appendCommandToTxBuffer(self):
        self.txBuffer.append(self.command)

    def appendDataToTxBuffer(self):
        self.txBuffer.append(self.data)
    
    def appendEOIToTxBuffer(self):
        self.txBuffer.append(self.data)

print("hello world")
comPort = serial.Serial("COM12")
comPort.close()
comPort.open()
message = "hello world\n"
comPort.write(bytes(message, "ascii"))
data = b'/x80/x00'
crc16 = crcmod.mkCrcFun(0x18005, rev=False, initCrc=0xFFFF, xorOut=0x0000)
crc = crc16(data)
print(hex(crc))
