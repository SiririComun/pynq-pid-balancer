from pynq import DefaultIP
from pynq.lib.iic import AxiIIC  # <--- Import the robust library
import math
import time

class MotorDriver(DefaultIP):
    # ... (Keep your MotorDriver exactly as it was, it works fine) ...
    def __init__(self, description):
        super().__init__(description)
        self.stop()

    def set_speed(self, value):
        val = max(0, min(value, 1023))
        hw_val = 1023 - val
        self.write(0x00, hw_val)

    def stop(self):
        self.set_speed(0)

MotorDriver.bindto = ['xilinx.com:ip:axi_gpio:2.0']


class MPU6050Driver(AxiIIC): # <--- Inherit from AxiIIC, not DefaultIP
    """
    Custom Driver for MPU6050.
    Inherits robust I2C logic from PYNQ and adds motion sensing methods.
    """
    def __init__(self, description):
        super().__init__(description)
        self._address = 0x68
        self._setup_sensor()

    def _setup_sensor(self):
        # Wake up MPU6050 using the robust .send() method
        self.send(self._address, bytes([0x6B, 0x00]), 2, 0)
        time.sleep(0.1)

    def read_word(self, reg):
        # 1. Send register address (with repeated start option=1)
        # Python 'bytes' is acceptable for sending
        self.send(self._address, bytes([reg]), 1, 1)
        
        # 2. Receive 2 bytes
        # REPLACEMENT: We must use the CFFI 'ffi' object from AxiIIC 
        # to create a buffer that the underlying C driver can write to.
        buf = AxiIIC._ffi.new("unsigned char[]", 2)
        self.receive(self._address, buf, 2, 0)
        
        # 3. Assemble and handle sign (Complement to 2)
        # We can index 'buf' just like a normal list
        value = (buf[0] << 8) | buf[1]
        if value >= 0x8000:
            value -= 65536
        return value

    def get_angle(self):
        # Read and scale axes using the hardware team's formula
        ax = self.read_word(0x3B) / 16384.0
        ay = self.read_word(0x3D) / 16384.0
        az = self.read_word(0x3F) / 16384.0
        
        # atan2(x, sqrt(y^2 + z^2)) * 180 / PI
        radians = math.atan2(ax, math.sqrt(ay**2 + az**2))
        return math.degrees(radians)

MPU6050Driver.bindto = ['xilinx.com:ip:axi_iic:2.1']