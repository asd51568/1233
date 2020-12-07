#!/usr/bin/env python3

from pynput.keyboard import Listener, Key, KeyCode
import asyncio
from mavsdk import System
 
store = set()
 
HOT_KEYS = {
    'run': set([ Key.alt_l, KeyCode(char='1')] )
}
 
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

    print("-- Landing")
    await drone.action.land()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
 
def handleKeyPress( key ):
    store.add( key )
 
    for action, trigger in HOT_KEYS.items():
        CHECK = all([ True if triggerKey in store else False for triggerKey in trigger ])
 
        if CHECK:
            try:
                func = eval( action )
                if callable( func ):
                   func()
            except NameError as err:
                print( err )
 
def handleKeyRelease( key ):
    if key in store:
        store.remove( key )
        
    if key == Key.esc:
        return False
 
with Listener(on_press=handleKeyPress, on_release=handleKeyRelease) as listener:
    listener.join()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())