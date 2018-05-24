from robotoPi import *

robot = RobotoPi()

sensor = Temperature(17)
temperatura = sensor.getTemperature()
humidade = sensor.getHumidity()

print("Humidade: "+str(humidade), "Temperatura: "+str(temperatura))

robot.exit()




