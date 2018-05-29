from robotoPi import *

robot = RobotoPi()
sensor = SensorColor(25, 23, 24)

while True:
    
    cor = sensor.getColor()
    print(cor)
    
robot.exit()




