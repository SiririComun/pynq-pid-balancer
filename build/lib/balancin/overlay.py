import os
from pynq import Overlay
from balancin.drivers import MotorDriver, MPU6050Driver

class BalancinOverlay(Overlay):
    """
    Custom Overlay class for the Balancin project.
    Handles automatic bitstream loading and provides a clean API to the IPs.
    """
    def __init__(self, bitfile_name="balancin.bit", **kwargs):
        # 1. Locate the bitstream relative to this file's location
        # This allows the package to work after it is installed in /usr/local/
        this_dir = os.path.dirname(__file__)
        bitfile_path = os.path.join(this_dir, 'bitstreams', bitfile_name)
        
        # 2. Initialize the base PYNQ Overlay
        # This flashes the FPGA and parses the .hwh
        super().__init__(bitfile_path, **kwargs)
        
        # 3. Explicitly map our custom drivers
        # We use the IP names from our Phase 0 discovery.
        # This solves the "Priority" issue where PYNQ defaults to generic drivers.
        self.motor = MotorDriver(self.ip_dict['axi_gpio_0'])
        self.sensor = MPU6050Driver(self.ip_dict['axi_iic_0'])

    def reset_hardware(self):
        """Safety method to put the hardware in a known safe state."""
        self.motor.stop()