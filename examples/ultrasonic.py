from robotoPi import * 

robot = RobotoPi()

ultrassonico = Ultrasonic(18, 24) #pino 18(trigger) e pino 24(echo)
distancia = ultrassonico.getDistance()

print(distancia)

robot.exit()




