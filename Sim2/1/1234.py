#!/usr/bin/env python

from dronekit import connect

# Connect to UDP endpoint.
vehicle = connect('127.0.0.1:14550', wait_ready=True)
# Use returned Vehicle object to query device state - e.g. to get the mode:
print("Mode: %s" % vehicle.mode.name)

vehicle = dronekit.connect('/dev/ttyS0')  # ... and other connection options
udp_conn = MAVConnection('udpin:0.0.0.0:15667', source_system=1)
vehicle._handler.pipe(udp_conn)
udp_conn.master.mav.srcComponent = 1  # needed to make QGroundControl work!
udp_conn.start()