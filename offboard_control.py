#!/usr/bin/env python3

import asyncio
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)
# import RPi.GPIO as GPIO
# import time


#좌표를 이용한 오프보드 제어
async def run():

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
       
    """   
    #Set GPIO numbering mode
    GPIO.setmode(GPIO.BOARD)

    #Set pin 11 as av output, and set servo1 as pin 11 as PWM
    GPIO.setup(11,GPIO.OUT)
    servo1 = GPIO.PWM(11,50) #Note 11 is pin, 50 = 50Hz pulse
    
    #start PWM running, but with value of 0 (pulse off)
    servo1 start(0)
    print ("waiting for 2 seconds")
    time.sleep(2)
    """

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
    
    """
    ##SERVO MOTOR
    while duty <= 12:
    servo1.ChangeDutyCycle(duty)
    time.sleep(1)
    duty = duty + 1
    #Turn back to 0 degrees
    servo1.ChangeDutyCycle(2)
    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)
    servo1.stop()
    GPIO.cleanup()
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
