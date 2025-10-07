## Move arm
import serial
import time

class MoveArm:
    def __init__(self):
        SERIAL_PORT = "/dev/ttyUSB0"
        BAUD_RATE = 115200
        TIMEOUT = 1
        ## Initialise serial port
        try:
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
            print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            exit(1)

        time.sleep(2)   ## Give MCU time to reset if needed (esp. if using USB-serial)
        self.setPause()

    def setPause(self, time = 1000):
        ## Give time in milliseconds
        self.movetime = time

    def reset(self) -> None:
        reset = 1500
        ## Double braces sends the entire command, removing it only sends servo 0
        resetting = "{{#000P{0:0>4d}T{1:0>4d}!#001P{0:0>4d}T{1:0>4d}!#002P{0:0>4d}T{1:0>4d}!#003P{0:0>4d}T{1:0>4d}!#004P{0:0>4d}T{1:0>4d}!#005P{0:0>4d}T{1:0>4d}!}}".format(reset, self.movetime)
        self.ser.write(resetting.encode())

        ## Pause to allow for movement completion
        time.sleep((self.movetime*2)/1000)

    def pause(self) -> None:
        time.sleep((self.movetime)/1000)

    def move(self, servo0 = 1500, servo1 = 1500, servo2 = 1500, servo3 = 1500, servo4 = 1500, servo5 = 1500) -> None:
        '''
        This method accounts for movement time between commands

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
        command = "{{#000P{0:0>4d}T{6:0>4d}!#001P{1:0>4d}T{6:0>4d}!#002P{2:0>4d}T{6:0>4d}!#003P{3:0>4d}T{6:0>4d}!#004P{4:0>4d}T{6:0>4d}!#005P{5:0>4d}T{6:0>4d}!}}".format(servo0, servo1, servo2, servo3, servo4, servo5, self.movetime)
        self.ser.write(command.encode())

        ## Pause to allow for movement completion
        time.sleep((self.movetime*2)/1000)

    def end(self) -> None:
        '''
        Closes serial connection, call at the end of process
        '''
        self.ser.close()
        print("Serial port closed")

