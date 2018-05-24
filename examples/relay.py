from robotoPi import *
import time

robot = RobotoPi()

rele = Relay(18)
print(rele.getPinNumber())


led.setOn()
print(rele.getState())

time.sleep(3)

rele.setOff()
print(rele.getState())


robot.exit()





