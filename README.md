# Balancin: Interactive PID Tuning Dashboard & Overlay

This repository contains the complete PYNQ-based hardware-software integration for the Balancin self-balancing project. It packages the FPGA hardware overlay, custom device drivers, and an asynchronous graphical dashboard for real-time PID tuning.

## Project Architecture

*   **Hardware Fabric (PL):** Runs the custom PWM motor IP and the hardware I2C master.
*   **Device Drivers (Python):** Custom classes (`MotorDriver` and `MPU6050Driver`) that extend PYNQ's base drivers to handle sensor physics (math formulas) and motor safety constraints (inverse logic).
*   **Threaded Control Manager:** An asynchronous control manager (`Balancer`) that executes the PID math at a stable 50Hz in a background thread, preventing Jupyter kernel freezes.
*   **Tuning Dashboard:** An interactive Jupyter interface featuring smooth real-time telemetry plots and dynamic gain sliders.

---

## Installation Guide (On PYNQ Board)

Open a terminal on your PYNQ board (connected to the internet) and execute the following commands:

### 1. Install the Package via Pip
Install the library and hardware binaries directly from this GitHub repository:
```bash
pip3 install git+https://github.com/SiririComun/pynq-pid-balancer.git