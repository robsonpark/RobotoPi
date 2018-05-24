from robotoPi import *

robot = RobotoPi()

sensor = Ldr(17)
intensidade_luz = sensor.getIntensity()

print("Luminosidade: "+str(intesidade_luz))

robot.exit()




