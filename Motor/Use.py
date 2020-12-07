#Import libraries
import RPi.GPIO as GPIO
import time

#Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

#Set pin 16 as TRIG and set pin 18 as ECHO
TRIG = 16
ECHO = 18


print ("Distance Measurement In Progress")

#Set TRIG as output and set ECHO as input
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
#Set pin 11 as av output, and set servo1 as pin 11 as PWM
GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50) #Note 11 is pin, 50 = 50Hz pulse
 
try:
  #start PWM running, but with value of 0 (pulse off)
    servo1.start(0)
    while True:
        
        GPIO.output(TRIG, False)
        time.sleep(0.5)
        
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        
        while GPIO.input(ECHO)==0:
            pulse_start = time.time()
        
        while GPIO.input(ECHO)==1:
            pulse_end = time.time()
        
        #Calculating Distance
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        #Print distance
        print ("Distance: ",distance,"cm")
        
        #거리에 맞게 서보모터를작동시키기
        if distance > 20:
            servo1.ChangeDutyCycle(2)
            time.sleep(0.5)
        elif distance > 17:
            servo1.ChangeDutyCycle(3)
            time.sleep(0.5)
        elif distance > 15:
            servo1.ChangeDutyCycle(4)
            time.sleep(0.5)
        elif distance > 10:
            servo1.ChangeDutyCycle(6)
            time.sleep(0.5)
        elif distance > 5:
            servo1.ChangeDutyCycle(8)
            time.sleep(0.5)
        else:
            servo1.ChangeDutyCycle(10)
            time.sleep(0.5)
        
except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program
    servo1.ChangeDutyCycle(2) 
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)
    print("Package Drop Success")
    servo1.stop()
    GPIO.cleanup()
