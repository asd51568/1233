#!/usr/bin/env python

import asyncio
from mavsdk import System
from pynput import keyboard

def on_release(key):
    if key == keyboard.Key.shift:
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
            
            return False

with keyboard.Listener(
    on_release=on_re) as listener:
    listener.join()

        
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())