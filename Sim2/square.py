#!/usr/bin/env python3

"""
Caveat when attempting to run the examples in non-gps environments:
`drone.offboard.stop()` will return a `COMMAND_DENIED` result because it
requires a mode switch to HOLD, something that is currently not supported in a
non-gps environment.
"""

import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)


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
