import serial
import time

class MoveCar:
    """
    This class defines methods to move the car portion of the carbot
    """
    def __init__(self):
        SERIAL_PORT = "/dev/ttyUSB0"   # Change if needed
        BAUD_RATE = 115200
        TIMEOUT = 1
        
        self.commands = {
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

        ## Initialise serial port
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
            print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            exit(1)

        time.sleep(2)  # Give MCU time to reset if needed (esp. if using USB-serial)
        self.setTime()

    def move(self, userCommand):
        """
        Move executes one command at a time, for the duration of motionTime

        Legal commands for movement:
        1. Forward
        2. Backward
        3. Left
        4. Right
        5. Left ish
        6. Right ish
        7. Stop

        Legal commands for tracking/detection:
        1. Avoid obs
        2. Follow
        """
        command = f"${self.commands[userCommand.upper()]}!"
        self.ser.write(command.encode())
        print(f"Sent: {userCommand.upper()} \t\t Duration: {self.motionTime}s")

        time.sleep(self.motionTime)

    def setTime(self, motionTime = 2):
        self.motionTime = motionTime
    
    def stop(self) -> None:
        command = f"${self.commands["STOP"]}!"
        self.ser.write(command.encode())
        print("Sent: STOP")

    def end(self) -> None:
        ## Stop all movement, in case self.stop was not called prior to end
        self.stop()
        self.ser.close()
        print("Serial port closed")
