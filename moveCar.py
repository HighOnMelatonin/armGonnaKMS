import serial
import time


COMMANDS = {
    "FORWARD":"QJ",
    "BACKWARD":"HT",
    "LEFT":"ZZ",
    "RIGHT":"YZ",
    "LEFT ISH":"ZPY",
    "RIGHT ISH":"YPY",
    "STOP":"TZ",
    "TRACKING":"ZNXJ",
    "AVOID OBS":"ZYBZ",
    "FOLLOW":"GSGN"
}

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

if __name__ == "__main__":
    # === Example: Send commands ===
    couts = ["TRACKING", "FOLLOW", "FORWARD", "RIGHT ISH", "BACKWARD"]

    for cout in couts:
        command = f"${COMMANDS[cout]}!"  # or whatever command your MCU expects
        ser.write(command.encode())   # Send string as bytes
        print(f"Sent: {cout.strip()}")
        time.sleep(2)   # Let command run for a while for observation

        # === Example: Read reply (if MCU sends one) ===
        try:
            response = ser.readline().decode().strip()
            if response:
                print(f"Received: {response}")
            else:
                print("No response received.")
        except Exception as e:
            print(f"Read error: {e}")


    # === Stop all commands ===
    command = f"${COMMANDS['STOP']}!"
    ser.write(command.encode())
    print(f"Sent: STOP")
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

