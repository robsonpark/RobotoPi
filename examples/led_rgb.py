from robotoPi import *
import time

robot = RobotoPi()

led = Led_RGB(17, 27, 22)

led.setColor("BLUE")
time.sleep(3)
led.setColor("RED")
time.sleep(3)
led.setColor("GREEN")
time.slepp(3)
led.setOff()

robot.exit()




