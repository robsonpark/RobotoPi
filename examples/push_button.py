from robotoPi import *
import time

robot = RobotoPi()

button = PushButton(23)

while True:
    time.sleep(0.1)
    print(button.getState())
    

robot.exit()
