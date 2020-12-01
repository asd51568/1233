# DroneKit, pymavlink, 기본 모듈 import
from dronekit import connect, Command, LocationGlobal
from pymavlink import mavutil
import time, sys, argparse, math 
# 기체 연결
print "Connecting"
connection_string = '127.0.0.1:14540'
vehicle = connect(connection_string, wait_ready=True)
# 기체 상태 표시
print " Type: %s" % vehicle._vehicle_type
print " Armed: %s" % vehicle.armed
print " System status: %s" % vehicle.system_status.state
print " GPS: %s" % vehicle.gps_0
print " Alt: %s" % vehicle.location.global_relative_frame.alt
