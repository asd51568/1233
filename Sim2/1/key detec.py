#!/usr/bin/env python3

import asyncio
from mavsdk import System
from pynput import keyboard

async def run():
            drone = System()
            await drone.connect(system_address="udp://:14540")

            print("Waiting for drone to connect...")
            async for state in drone.core.connection_state():
                if state.is_connected:
                    print(f"Drone discovered with UUID: {state.uuid}")
                    break

            print("Waiting for drone to have a global position estimate...")
            async for health in drone.telemetry.health():
                if health.is_global_position_ok:
                    print("Global position estimate ok")
                    break
            print("-- Arming")
            await drone.action.arm()

            print("-- Taking off")
            await drone.action.takeoff()
            await asyncio.sleep(10)

def on_release(key):

with keyboard.Listener( 
    on_press=on_press, 
    on_release=on_release) as listener:
    listener.join()

if __name__ == "__main__":
    if key == keyboard.Key.shift:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run())