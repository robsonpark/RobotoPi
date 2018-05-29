__author__ = "Robson Soares"
__copyright__ = "Copyright 2018"

__license__ = ""
__version__ = "1.0"
__maintainer__ = "Robson Soares"
__email__ = "robson.soares@dce.ufpb.br"
__status__ = "Development"

'''
Requeriments:

sudo apt-get install python-dev python-rpi.gpio espeak

git clone https://github.com/adafruit/Adafruit_Python_DHT.git

https://github.com/nickcoutsos/MPU-6050-Python

'''

import RPi.GPIO as GPIO
import Adafruit_DHT
import smbus
import time
import os

class RobotoPi():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)
    def exit(self):
        GPIO.cleanup()
        exit()

class Accelerometer:

    # Global Variables
    GRAVITIY_MS2 = 9.80665
    address = None
    bus = smbus.SMBus(1)

    # Scale Modifiers
    ACCEL_SCALE_MODIFIER_2G = 16384.0
    ACCEL_SCALE_MODIFIER_4G = 8192.0
    ACCEL_SCALE_MODIFIER_8G = 4096.0
    ACCEL_SCALE_MODIFIER_16G = 2048.0

    GYRO_SCALE_MODIFIER_250DEG = 131.0
    GYRO_SCALE_MODIFIER_500DEG = 65.5
    GYRO_SCALE_MODIFIER_1000DEG = 32.8
    GYRO_SCALE_MODIFIER_2000DEG = 16.4

    # Pre-defined ranges
    ACCEL_RANGE_2G = 0x00
    ACCEL_RANGE_4G = 0x08
    ACCEL_RANGE_8G = 0x10
    ACCEL_RANGE_16G = 0x18

    GYRO_RANGE_250DEG = 0x00
    GYRO_RANGE_500DEG = 0x08
    GYRO_RANGE_1000DEG = 0x10
    GYRO_RANGE_2000DEG = 0x18

    # MPU-6050 Registers
    PWR_MGMT_1 = 0x6B
    PWR_MGMT_2 = 0x6C

    SELF_TEST_X = 0x0D
    SELF_TEST_Y = 0x0E
    SELF_TEST_Z = 0x0F
    SELF_TEST_A = 0x10

    ACCEL_XOUT0 = 0x3B
    ACCEL_XOUT1 = 0x3C
    ACCEL_YOUT0 = 0x3D
    ACCEL_YOUT1 = 0x3E
    ACCEL_ZOUT0 = 0x3F
    ACCEL_ZOUT1 = 0x40

    TEMP_OUT0 = 0x41
    TEMP_OUT1 = 0x42

    GYRO_XOUT0 = 0x43
    GYRO_XOUT1 = 0x44
    GYRO_YOUT0 = 0x45
    GYRO_YOUT1 = 0x46
    GYRO_ZOUT0 = 0x47
    GYRO_ZOUT1 = 0x48

    ACCEL_CONFIG = 0x1C
    GYRO_CONFIG = 0x1B

    def __init__(self, address):
        self.address = address

        # Wake up the MPU-6050 since it starts in sleep mode
        self.bus.write_byte_data(self.address, self.PWR_MGMT_1, 0x00)

    # I2C communication methods

    def read_i2c_word(self, register):
        """Read two i2c registers and combine them.
        register -- the first register to read from.
        Returns the combined read results.
        """
        # Read the data from the registers
        high = self.bus.read_byte_data(self.address, register)
        low = self.bus.read_byte_data(self.address, register + 1)

        value = (high << 8) + low

        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else:
            return value

    # MPU-6050 Methods

    def get_temp(self):
     
        # Get the raw data
        raw_temp = self.read_i2c_word(self.TEMP_OUT0)

        # Get the actual temperature using the formule given in the
        # MPU-6050 Register Map and Descriptions revision 4.2, page 30
        actual_temp = (raw_temp / 340) + 36.53

        # Return the temperature
        return actual_temp

    def set_accel_range(self, accel_range):
       
        
        # First change it to 0x00 to make sure we write the correct value later
        self.bus.write_byte_data(self.address, self.ACCEL_CONFIG, 0x00)

        # Write the new range to the ACCEL_CONFIG register
        self.bus.write_byte_data(self.address, self.ACCEL_CONFIG, accel_range)

    def read_accel_range(self, raw = False):
        
        # Get the raw value
        raw_data = self.bus.read_byte_data(self.address, self.ACCEL_CONFIG)

        if raw is True:
            return raw_data
        elif raw is False:
            if raw_data == self.ACCEL_RANGE_2G:
                return 2
            elif raw_data == self.ACCEL_RANGE_4G:
                return 4
            elif raw_data == self.ACCEL_RANGE_8G:
                return 8
            elif raw_data == self.ACCEL_RANGE_16G:
                return 16
            else:
                return -1

    def get_accel_data(self, g = False):
       
        # Read the data from the MPU-6050
        x = self.read_i2c_word(self.ACCEL_XOUT0)
        y = self.read_i2c_word(self.ACCEL_YOUT0)
        z = self.read_i2c_word(self.ACCEL_ZOUT0)

        accel_scale_modifier = None
        accel_range = self.read_accel_range(True)

        if accel_range == self.ACCEL_RANGE_2G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G
        elif accel_range == self.ACCEL_RANGE_4G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_4G
        elif accel_range == self.ACCEL_RANGE_8G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_8G
        elif accel_range == self.ACCEL_RANGE_16G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_16G
        else:
            print("Unkown range - accel_scale_modifier set to self.ACCEL_SCALE_MODIFIER_2G")
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G

        x = x / accel_scale_modifier
        y = y / accel_scale_modifier
        z = z / accel_scale_modifier

        if g is True:
            return {'x': x, 'y': y, 'z': z}
        elif g is False:
            x = x * self.GRAVITIY_MS2
            y = y * self.GRAVITIY_MS2
            z = z * self.GRAVITIY_MS2
            return {'x': x, 'y': y, 'z': z}

    def set_gyro_range(self, gyro_range):
        
        # First change it to 0x00 to make sure we write the correct value later
        self.bus.write_byte_data(self.address, self.GYRO_CONFIG, 0x00)

        # Write the new range to the ACCEL_CONFIG register
        self.bus.write_byte_data(self.address, self.GYRO_CONFIG, gyro_range)

    def read_gyro_range(self, raw = False):
        
        raw_data = self.bus.read_byte_data(self.address, self.GYRO_CONFIG)

        if raw is True:
            return raw_data
        elif raw is False:
            if raw_data == self.GYRO_RANGE_250DEG:
                return 250
            elif raw_data == self.GYRO_RANGE_500DEG:
                return 500
            elif raw_data == self.GYRO_RANGE_1000DEG:
                return 1000
            elif raw_data == self.GYRO_RANGE_2000DEG:
                return 2000
            else:
                return -1

    def get_gyro_data(self):
        
        # Read the raw data from the MPU-6050
        x = self.read_i2c_word(self.GYRO_XOUT0)
        y = self.read_i2c_word(self.GYRO_YOUT0)
        z = self.read_i2c_word(self.GYRO_ZOUT0)

        gyro_scale_modifier = None
        gyro_range = self.read_gyro_range(True)

        if gyro_range == self.GYRO_RANGE_250DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG
        elif gyro_range == self.GYRO_RANGE_500DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_500DEG
        elif gyro_range == self.GYRO_RANGE_1000DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_1000DEG
        elif gyro_range == self.GYRO_RANGE_2000DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_2000DEG
        else:
            print("Unkown range - gyro_scale_modifier set to self.GYRO_SCALE_MODIFIER_250DEG")
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG

        x = x / gyro_scale_modifier
        y = y / gyro_scale_modifier
        z = z / gyro_scale_modifier

        return {'x': x, 'y': y, 'z': z}

    def get_all_data(self):
        """Reads and returns all the available data."""
        temp = self.get_temp()
        accel = self.get_accel_data()
        gyro = self.get_gyro_data()

        return [accel, gyro, temp]

class PushButton():
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        GPIO.setup(self.pinNumber, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        
    #This method return True to pressed and False to unpressed
    def getState(self):
        if(GPIO.input(self.pinNumber)==1):
            return False
        else:
            return True
    #This method return the pin number associated
    def getPinNumber(self):
        return self.pinNumber
    
class Led():
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        self.state = False
        GPIO.setup(pinNumber,GPIO.OUT)
        
    def getPinNumber(self):
        return self.pinNumber
    
    def setOn(self):
        GPIO.output(self.pinNumber,GPIO.HIGH)
        self.state = True
        
    def setOff(self):
        GPIO.output(self.pinNumber,GPIO.LOW)
        self.state = False
        
    def getState(self):
        return self.state
class Ldr():
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        GPIO.setup(self.pinNumber, GPIO.OUT)
    def intensity (self):
        count = 0
        GPIO.output(self.pinNumber, GPIO.LOW)
        time.sleep(0.1)
        GPIO.setup(self.pinNumber, GPIO.IN)
    
        while (GPIO.input(self.pinNumber) == GPIO.LOW):
            count += 1

        return count
class Infrared():
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        GPIO.setup(self.pinNumber,GPIO.IN)

    def getState(self):
        return GPIO.input(self.pinNumber)
class Relay():
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        self.state = False
        GPIO.setup(pinNumber,GPIO.OUT)
        
    def getPinNumber(self):
        return self.pinNumber
    
    def setOn(self):
        GPIO.output(self.pinNumber,GPIO.HIGH)
        self.state = True
        
    def setOff(self):
        GPIO.output(self.pinNumber,GPIO.LOW)
        self.state = False
        
    def getState(self):
        return self.state     

class Temperature():
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        self.sensor = Adafruit_DHT.DHT22
        GPIO.setup(self.pinNumber, GPIO.IN)
    def getTemperature(self):
        humid, temp = Adafruit_DHT.read_retry(self.sensor, self.pinNumber);
        return temp

    def getHumidity(self):
        humid, temp = Adafruit_DHT.read_retry(self.sensor, self.pinNumber);
        return humid
class Motor():
    def __init__(self, enablePin, inputPin1, inputPin2):
        self.enablePin = enablePin    
        self.inputPin1 = inputPin1
        self.inputPin2 = inputPin2
        
        GPIO.setup(self.enablePin, GPIO.OUT)
        GPIO.setup(self.inputPin1, GPIO.OUT)
        GPIO.setup(self.inputPin2, GPIO.OUT)
        self.motor_pwm = GPIO.PWM(self.enablePin, 500)
        self.motor_pwm.start(0)
    def forward(self, duty):          
        GPIO.output(self.inputPin1, True) 
        GPIO.output(self.inputPin2, False) 
        self.motor_pwm.ChangeDutyCycle(duty)
        
    def reverse(self, duty):          
        GPIO.output(self.inputPin1, False) 
        GPIO.output(self.inputPin2, True) 
        self.motor_pwm.ChangeDutyCycle(duty)    
    
    def stop(self):
        GPIO.output(self.inputPin1, False) 
        GPIO.output(self.inputPin2, False) 
        self.motor_pwm.ChangeDutyCycle(0)

class ServoMotor():
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        
        deg_0_pulse   = 0.5 
        deg_180_pulse = 2.5
        f = 50.0
        
        period = 1000/f
        k = 100/period
        self.deg_0_duty = deg_0_pulse*k
        pulse_range = deg_180_pulse - deg_0_pulse
        self.duty_range = pulse_range * k
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servo_pin,GPIO.OUT)
        self.pwm = GPIO.PWM(servo_pin,f)
        self.pwm.start(0)
    def setAngle(self, angle):
        duty = self.deg_0_duty + (angle/180.0)* self.duty_range
        self.pwm.ChangeDutyCycle(self.duty)
    def stop(self):
        self.pwm.stop()

class Ultrasonic():
    def __init__(self, pinTrigger, pinEcho):
        self.pinTrigger = pinTrigger
        self.pinEcho = pinEcho
        GPIO.setup(self.pinTrigger, GPIO.OUT)
        GPIO.setup(self.pinEcho, GPIO.IN)
     
    def getDistance(self):
        GPIO.output(self.pinTrigger, True)
        time.sleep(0.00001)
        GPIO.output(self.pinTrigger, False)
     
        StartTime = time.time()
        StopTime = time.time()
     
        while GPIO.input(self.pinEcho) == 0:
            StartTime = time.time()
     
        while GPIO.input(self.pinEcho) == 1:
            StopTime = time.time()
     
        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2
     
        return distance
class Led_RGB():
    def __init__(self, inputPin1, inputPin2, inputPin3):
        self.inputPin1 = inputPin1
        self.inputPin2 = inputPin2
        self.inputPin3 = inputPin3
        self.color = "WHITE"

        GPIO.setup(self.inputPin1,GPIO.OUT)
        GPIO.output(self.inputPin1,0)
        GPIO.setup(self.inputPin2,GPIO.OUT)
        GPIO.output(self.inputPin2,0)
        GPIO.setup(self.inputPin3,GPIO.OUT)
        GPIO.output(self.inputPin3,0)
        
    def setColor(self, color):
        
        if(color=="BLUE"):
            GPIO.output(self.inputPin1,0)
            GPIO.output(self.inputPin2,0)
            GPIO.output(self.inputPin3,1)
            self.color = "BLUE"
        elif(color=="GREEN"):
            GPIO.output(self.inputPin1,0)
            GPIO.output(self.inputPin2,1)
            GPIO.output(self.inputPin3,0)
            self.color = "GREEN"
        elif(color=="RED"):
            GPIO.output(self.inputPin1,1)
            GPIO.output(self.inputPin2,0)
            GPIO.output(self.inputPin3,0)
            self.color = "RED"
        else:
            GPIO.output(self.inputPin1,0)
            GPIO.output(self.inputPin2,0)
            GPIO.output(self.inputPin3,0)
            self.color = "OFF"
    def getColor(self, color):
        return self.color
    def setOff(self):
        GPIO.output(self.inputPin1,0)
        GPIO.output(self.inputPin2,0)
        GPIO.output(self.inputPin3,0)
        self.color = "OFF"


class Voice():
    def __init__(self, lang):
        self.lang = lang
    def speak(text, self):
        os.system("espeak -v "+lang+" \""+text+"\"")
class Camera():
    def __init__(self):
        pass
class ColorSensor():
    def __init__(self, signal, s2, s3):
        self.signal = signal
        self.s2 = s2
        self.s3 = s3
        GPIO.setup(signal,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(s2,GPIO.OUT)
        GPIO.setup(s3,GPIO.OUT)

    def getColor(self):
        temp = 1
        
        GPIO.output(self.s2,GPIO.LOW)
        GPIO.output(self.s3,GPIO.LOW)
        time.sleep(0.3)
        start = time.time()
        
        for impulse_count in range(NUM_CYCLES):
            GPIO.wait_for_edge(self.signal, GPIO.FALLING)
        duration = time.time() - start 
        red  = NUM_CYCLES / duration   
   
        GPIO.output(self.s2,GPIO.LOW)
        GPIO.output(self.s3,GPIO.HIGH)
        time.sleep(0.3)
        start = time.time()
        
        for impulse_count in range(NUM_CYCLES):
            GPIO.wait_for_edge(self.signal, GPIO.FALLING)
        duration = time.time() - start
        blue = NUM_CYCLES / duration
        

        GPIO.output(self.s2,GPIO.HIGH)
        GPIO.output(self.s3,GPIO.HIGH)
        time.sleep(0.3)
        start = time.time()
        
        for impulse_count in range(NUM_CYCLES):
            GPIO.wait_for_edge(self.signal, GPIO.FALLING)
        duration = time.time() - start
        green = NUM_CYCLES / duration
        
          
        if green<7000 and blue<7000 and red>12000:
            temp=1
            return("red")
        elif red<12000 and  blue<12000 and green>12000:
            
            temp=1
            return("green")
        elif green<7000 and red<7000 and blue>12000:
            
            temp=1
            return("blue")
        elif red>10000 and green>10000 and blue>10000 and temp==1:
            temp=0
            return("No color")




















        
