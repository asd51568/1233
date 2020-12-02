#실제 사용할 예정인 코드
  
import RPi.GPIO as GPIO 
from time import sleep  

servoPin          = 12   
SERVO_MAX_DUTY    = 12   
SERVO_MIN_DUTY    = 3   

GPIO.setmode(GPIO.BOARD)        
GPIO.setup(servoPin, GPIO.OUT)  

servo = GPIO.PWM(servoPin, 50)  
servo.start(0)  

def setServoPos(degree):
  if degree > 180:
    degree = 180

  duty = SERVO_MIN_DUTY+(degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
  print("Degree: {} to {}(Duty)".format(degree, duty))

  servo.ChangeDutyCycle(duty)
  
def main()
  setServoPos(180)  #서보를 작동하여 고리를 걸수있게 위치를 조정
  sleep(물건이 정해진위치에 도달했을때까지)
  
  setServoPos(90)
  sleep(기체가 목표지점에 도착하기 전까지)
  
  setServoPos(180)    #고리에 걸려잇던 물건 낙하
  sleep(10)    #확실하게 물건이 낙하할때까지 대기
  
  servo.stop()
  GPIO.cleanup()
  
if __name__ == "__main__":  
  main()
  
#참고자료1
#https://www.youtube.com/watch?v=xHDT4CwjUQE
#Import libraries
import RPi.GPIO as GPIO
import time

#Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

#Set pin 11 as av output, and set servo1 as pin 11 as PWM
GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50) #Note 11 is pin, 50 = 50Hz pulse

#start PWM running, but with value of 0 (pulse off)
servo1 start(0)
print ("waiting for 2 seconds")
time.sleep(2)

#Let's move the servo!
print ("Rotating 180 degrees in 10 steps")

#Define variable duty
duty = 2

#Loop for duty values from 2 to 12 (0 to 180 degrees)
while duty <= 12:
  servo1.ChangeDutyCycle(duty)
  time.sleep(1)
  duty = duty + 1
  
#Wait a couple of seconds
time.sleep(2)

#Turn back to 90 degrees
print ("Turning back to 90 degrees for 2 seconds")
servo1.ChangeDutyCycle(7)
time.sleep(2)

#Turn back to 0 degrees
print ("Turning back to 0 degrees")
servo1.ChangeDutyCycle(2)
time.sleep(0.5)
servo1.ChangeDutyCycle(0)

#Clean things up at the end
servo1.stop()
GPIO.cleanup()
print ("Goodbye")

#2
#Import libraries
import RPi.GPIO as GPIO
import time

#Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

#Set pin 11 as av output, and set servo1 as pin 11 as PWM
GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50) #Note 11 is pin, 50 = 50Hz pulse

#start PWM running, but with value of 0 (pulse off)
servo1 start(0)

#Loop to allow user to set servo angle. Try/finally allows exit
#with execution of servo. stop and GPIO cleanup

try:
  while True:
    #Ask user for angle and turn servo to it
    angle = float(input('Enter angle between 0 & 180: '))
    servo1.ChangeDutyCycle(2+(angle/18))
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)
    
finally:
  #Clean things up at the end
  servo1.stop()
  GPIO.cleanup()
  print("Goodbye!")
