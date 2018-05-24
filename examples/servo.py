from robotoPi import *
import time

robot = RobotoPi()

servo = ServoMotor(17)

servo.setAngle(30)
time.sleep(3)
servo.setAngle(45)
time.sleep(3)
servo.setAngle(60)
time.sleep(3)
servo.setAngle(90)
time.sleep(3)
servo.setAngle(180)
time.sleep(3)
servo.setAngle(270)

servo.stop()

robot.exit()




