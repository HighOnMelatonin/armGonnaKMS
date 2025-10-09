from MoveArm import MoveArm
from MoveCar import MoveCar

def main():
    armMotion = MoveArm()
    carMotion = MoveCar()

    ## 2500 to 500
    servo0 = 1000

    ## 2500 to 700 (physical limit, 500 mechanical limit)
    servo1 = 900
    
    ## 2500 to 550 (physical limit, 500 mechanical limit)
    servo2 = 900

    ## 
    servo3 = 2000
    servo4 = 1500
    servo5 = 1500

    armMotion.setPause(1500)
    armMotion.move(servo0, servo1, servo2, servo3, servo4, servo5)
    
    armMotion.move(servo0 - 50, servo1 + 40, servo2 -60, servo3 + 100, servo4, servo5 + 1000)
    
    #carMotion.end()

    armMotion.move()
    armMotion.end()

if __name__ == "__main__":
    main()

    
