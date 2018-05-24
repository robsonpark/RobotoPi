from robotoPi import *

robot = RobotoPi()

infravermelho = Infrared(17)
estado = infravermelho.getState()

print(estado)

robot.exit()




