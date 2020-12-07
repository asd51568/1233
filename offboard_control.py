#!/usr/bin/env python3
import asyncio
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)
# import RPi.GPIO as GPIO
# import time

"""
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
    servo1 start(0)
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
        """

async def run():
    """ Does Offboard control using position NED coordinates. """

    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("-- 시동")
    await drone.action.arm()
    
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- offboard control 시작")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    print("-- 고도 10m 상승")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -10.0, 0.0))
    await asyncio.sleep(10)

    print("-- 10m 전진")
    await drone.offboard.set_position_ned(PositionNedYaw(10.0, 0.0, -10.0, 0.0))
    await asyncio.sleep(3)
    
    print("-- 90도 우측 회전 후 전진")
    await drone.offboard.set_position_ned(PositionNedYaw(10.0, 0.0, -10.0, 90.0))
    await asyncio.sleep(1)
    await drone.offboard.set_position_ned(PositionNedYaw(10.0, 10.0, -10.0, 90.0))
    await asyncio.sleep(3)

    print("-- 배송지 도착 : 착륙")
    await drone.offboard.set_position_ned(PositionNedYaw(10.0, 10.0, 0.0, 90.0))
    await asyncio.sleep(15)
    ##--SERVO CODE
    """
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
    """
    
    print("-- 배송 완료 : 이륙")
    await drone.offboard.set_position_ned(PositionNedYaw(10.0, 10.0, -10.0, 90.0))
    await asyncio.sleep(10)
    
    print("-- 90도 우측 회전 후 전진")
    await drone.offboard.set_position_ned(PositionNedYaw(10.0, 10.0, -10.0, 180.0))
    await asyncio.sleep(1)
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 10.0, -10.0, 180.0))
    await asyncio.sleep(3)

    print("-- offboard 종료 : RTL")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
