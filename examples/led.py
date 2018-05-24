from robotoPi import *
import time

robot = RobotoPi()

led = Led(18)
print(led.getPinNumber())


led.setOn()
print(led.getState())

time.sleep(3)

led.setOff()
print(led.getState())


robot.exit()
