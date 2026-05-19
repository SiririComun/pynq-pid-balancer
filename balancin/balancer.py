import threading
import time
from collections import deque
from balancin.pid import PID

class Balancer:
    """
    Main manager for the balancing logic.
    Runs the PID loop in a background thread.
    """
    def __init__(self, overlay, kp=3.5, ki=0.0, kd=0.0):
        self.ol = overlay
        self.pid = PID(kp, ki, kd, out_min=-500, out_max=500)
        
        # Control parameters
        self.target_angle = 20.0  # The "Referencia"
        self.base_pwm = 500       # The "PWM_BASE"
        
        # Threading control
        self.running = False
        self._thread = None
        
        # Add a rolling buffer for the last 100 samples
        self.history = deque(maxlen=100)
            
    def _loop(self):
        last_time = time.perf_counter()
        while self.running:
            now = time.perf_counter()
            dt = now - last_time
            last_time = now
            
            current_angle = self.ol.sensor.get_angle()
            correction = self.pid.compute(self.target_angle, current_angle, dt)
            
            self.ol.motor.set_speed(int(self.base_pwm + correction))
           
            self.history.append((now, current_angle, self.target_angle))
            
            time.sleep(0.02)

    def start(self):
        """Starts the background thread."""
        if not self.running:
            self.running = True
            self.pid.reset()
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()
            print("Balancer thread started.")

    def stop(self):
        """Safely stops the thread and the motor."""
        self.running = False
        if self._thread:
            self._thread.join()
        self.ol.motor.stop()
        print("Balancer stopped and motor safety shutdown complete.")

    def set_params(self, kp=None, ki=None, kd=None, target=None, base=None):
        """Updates parameters in real-time while the thread is running."""
        if kp is not None: self.pid.kp = kp
        if ki is not None: self.pid.ki = ki
        if kd is not None: self.pid.kd = kd
        if target is not None: self.target_angle = target
        if base is not None: self.base_pwm = base