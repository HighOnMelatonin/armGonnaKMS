## Move arm
import serial
import time

class MoveArm:
    """
    This class defines methods to move the arm portion of the carbot
    """
    def __init__(self):

        SERIAL_PORT = "/dev/ttyUSB0"
        BAUD_RATE = 115200
        TIMEOUT = 1
        ## Initialise serial port
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
            print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            exit(1)

        time.sleep(2)   ## Give MCU time to reset if needed (esp. if using USB-serial)
        self.setPause()

    def setPause(self, time = 1000):
        ## Give time in milliseconds
        self.movetime = time

    def pause(self) -> None:
        time.sleep((self.movetime)/1000)

    def move(self, servo0 = 1500, servo1 = 1500, servo2 = 1500, servo3 = 1500, servo4 = 1500, servo5 = 1500) -> None:
        '''
        This method accounts for movement time between commands, default values are 1500 PWM
        Calling this method with no values provided will reset the robot to the default position

        Servo 0 (waist):
        Lower limit: 0
        Upper limit: 3000

        Servo 1

        Servo 2
        
        Servo 3

        Servo 4 (Wrist)
        
        Servo 5 (Fingers)
        '''
        print("Moving arm")
        print(f"Servo 0: {servo0}\nServo 1: {servo1}\nServo 2: {servo2}\nServo 3: {servo3}\nServo 4: {servo4}\nServo 5: {servo5}")
        command = f"{{#000P{servo0:0>4d}T{self.movetime:0>4d}!#001P{servo1:0>4d}T{self.movetime:0>4d}!#002P{servo2:0>4d}T{self.movetime:0>4d}!#003P{servo3:0>4d}T{self.movetime:0>4d}!#004P{servo4:0>4d}T{self.movetime:0>4d}!#005P{servo5:0>4d}T{self.movetime:0>4d}!}}"
        self.ser.write(command.encode())

        ## Pause to allow for movement completion
        time.sleep((self.movetime*2)/1000)

    def end(self) -> None:
        '''
        Closes serial connection, call at the end of process
        '''
        self.ser.close()
        print("Serial port closed")

