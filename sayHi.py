import serial
import time

# === Configuration ===
SERIAL_PORT = "/dev/ttyUSB0"   # Change if needed
BAUD_RATE = 115200             # Must match your MCU firmware setting
TIMEOUT = 1                    # 1 second read timeout

# === Initialize Serial Port ===
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

time.sleep(2)  # Give MCU time to reset if needed (esp. if using USB-serial)

# === Example: Send command ===
cout = "FORWARD!!"
command = "$QJ!"  # or whatever command your MCU expects
ser.write(command.encode())   # Send string as bytes
print(f"Sent: {cout.strip()}")

# === Example: Read reply (if MCU sends one) ===
try:
    response = ser.readline().decode().strip()
    if response:
        print(f"Received: {response}")
    else:
        print("No response received.")
except Exception as e:
    print(f"Read error: {e}")

# === Clean up ===
ser.close()
print("Serial port closed.")

