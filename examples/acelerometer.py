from robotoPi import *

robot = RobotoPi()
sensor = Accelerometer(0x68)

while True:
    
    accel_data = sensor.get_accel_data()
    gyro_data = sensor.get_gyro_data()
    temp = sensor.get_temp()

    print("Dados do acelerômetro")
    print("x: " + str(accel_data['x']))
    print("y: " + str(accel_data['y']))
    print("z: " + str(accel_data['z']))

    print("Dados do giroscópio")
    print("x: " + str(gyro_data['x']))
    print("y: " + str(gyro_data['y']))
    print("z: " + str(gyro_data['z']))

    print("Temperatura: " + str(temp) + " C")
    sleep(0.5)

robot.exit()




