import pigpio
from time import sleep
import codecs

class AMT203():
    def __init__(self, bus=0, deviceId=0, baud_rate=1000000):
        self.deviceId = deviceId
        self.bus = bus
        self.pi = pigpio.pi()
        self.baud_rate = baud_rate

        try:
            print "bus: %s | pin: %s" % (self.bus, self.deviceId)
            self.spi = self.pi.spi_open(0,self.baud_rate)
            self.open = True
            print "SPI connected. Device id: ", self.deviceId
        except Exception as e:
            self.open = False
            print "Could not connect to SPI device: ", e

    def clean_buffer(self):
        first_result = self.pi.spi_xfer(self.spi,[0x00])
        while first_result[1] != b'\xa5':
          print first_result 
          first_result = self.pi.spi_xfer(self.spi,[0x00])
        print "Buffer empty"
    def get_position(self):
        first_result = self.pi.spi_xfer(self.spi,[0x10])
        while first_result[1] != b'\x10':
          first_result = self.pi.spi_xfer(self.spi,[0x00])
        discard, msb_result = self.pi.spi_xfer(self.spi,[0x00])
        discard2, lsb_result = self.pi.spi_xfer(self.spi,[0x00])
        print "MSB: %s | LSB: %s " % (msb_result, lsb_result)
        print msb_result
        msb = self.bytes_to_int(msb_result)
        lsb = self.bytes_to_int(lsb_result)
        # msb_bin = bin(msb_result[0]<<8)[2:]
        # lsb_bin = bin(lsb_result[0])[2:]
        final_result = (msb]<<8 | lsb[1])
        # print "Final: ", final_result
        self.clean_buffer()
        return final_result
    def set_zero(self):
        self.clean_buffer()
        first_result = self.pi.spi_xfer(self.spi,[0x70])
        while first_result[1] != b'\x80':
          print first_result
          first_result = self.pi.spi_xfer(self.spi,[0x00])
        print "Zero set was successful and the new position offset is stored in EEPROM"
        self.clean_buffer()
        # GPIO.output(self.pin, GPIO.LOW)
        sleep(0.1)
        # GPIO.output(self.pin, GPIO.HIGH)

    def get_resolution(self):
        return 4096
    def bytes_to_int(value):
        return int(codecs.encode(value,'hex'), 16)