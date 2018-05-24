from robotoPi import * 
import time

robot = RobotoPi()
velocidade = 100

motor1 = Motor(17, 27)
motor2 = Motor(22, 23) 

motor1.foward(velocidade)
motor2.foward(velocidade)

time.sleep(3)

motor1.reverse(velocidade)
motor2.reverse(velocidade)

time.sleep(3)

motor1.stop()
motor2.stop()

robot.exit()




