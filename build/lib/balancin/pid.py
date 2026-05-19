import time

class PID:
    """
    Generic PID Controller.
    Separates control logic from hardware communication.
    """
    def __init__(self, kp, ki, kd, out_min=0, out_max=1023):
        # Gain constants
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        # Output limits (PWM range)
        self.out_min = out_min
        self.out_max = out_max
        
        # Internal state
        self.integral = 0
        self.last_error = 0
        
    def compute(self, setpoint, measured_value, dt):
        """
        Calculates the PID output.
        dt: The actual time elapsed since the last calculation.
        """
        # Calculate error
        error = setpoint - measured_value
        
        # Proportional term
        p_term = self.kp * error
        
        # Integral term with Anti-Windup
        # We limit the integral so it doesn't grow to infinity if the motor is stuck
        self.integral += error * dt
        self.integral = max(min(self.integral, 200), -200) # Simple clamp
        i_term = self.ki * self.integral
        
        # Derivative term
        # (Change in error / time)
        d_term = self.kd * (error - self.last_error) / dt
        
        # Total output
        output = p_term + i_term + d_term
        
        # Save state for next iteration
        self.last_error = error
        
        return output

    def set_tunings(self, kp, ki, kd):
        """Allows real-time updates of constants."""
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def reset(self):
        """Clears memory of previous errors."""
        self.integral = 0
        self.last_error = 0