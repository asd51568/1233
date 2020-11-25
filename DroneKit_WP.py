# DroneKit, pymavlink, 기본 모듈 import
from dronekit import connect, Command, LocationGlobal, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time, sys, argparse, math 

#--시동 및 이륙
def arm_and_takeoff(altitude):

def clear_mission(vehicle):
    #-초기화
    cmds = vehicle.commands
    cmds.clear()
    vehicle.flush()
    
    #-mission 다운로드
    cmds.download()
    cmds.wait_ready()

def download_mission(vehicle):
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()

def get_current_mission():
    #-현재 미션 다운로드, wp와 list 갯수 
    print ("Downloading the mission")
    download_mission(vehicle)
    missionList = []
    n_wp = 0

    for wp in vehicle.commands:
        missionList.append(wp)
        n_wp += 1
    
    return n_wp, missionList


def add_last_waypoint_to_mission(vehicle, lat, long, alt):
    #-wp, list 추가
    download_mission()
    cmds = download_mission(vehicle)

    #-임시 list 저장
    missionList = []
    for wp in cmds:
        missionList.append (wp)
    
    #-마지막 경유지 추가
    wp_last = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, lat, long, alt)
    missionList.append(wp_last)

    #-현재 mission 삭제
    cmds.clear()

    #-새로운 mission 추가
    for wp in missionList:
        cmds.add(wp)
    
    cmds.upload()

    return (cmds.count)

def ChangeMode(vehicle, mode):
    #-모드변경

    while vehicle.mode != Vehicle(Mode):
        vehicle.mode = VehicleMode(mode)
        time.sleep(0.5)

    return True


#----초기화
gnd_speed = 10
mode = 'GROUND'

#----연결
##---parameter 체크
vehicle = connect('udp:127.0.0.1:14540')

#----main 함수
while True:
    if mode == 'GROUND':
        #--mission 업로드 대기
        n_wp, missionList = get_current_mission(vehicle)
        time.sleep(2)

        if n_wp > 0:
            print ("A valid mission has been uploaded: takeoff")
            mode = 'TAKEOFF'
    
    elif mode == 'TAKEOFF':
        #--RTL
        add_last_waypoint_to_mission(vehicle, vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, vehicle.location.global_relative_frame.alt)
        
        print ("Final waypoint added to the current mission")
        time.sleep (1)

        #--Takeoff
        arm_and_takeoff(10)

        #--모드 변경
        ChangeMode(vehicle, "AUTO")

        #--속도설정
        vehicle.groundspeed = gnd_speed

        mode = "MISSION"
        print("Switch to MISSION mode")

    elif mide == 'MISSION':
        #--RTL 후 LANDING

        print("Current WP: %d of %d "%(vehicle.commands.next, vehicle.commands.count))

        if (vehicle.commands.next == vehicle.commands.count):
            print ("Final wp reached: go back home")

            #--미션 완료
            clear_mission(vehicle)
            print ("Mission deleted")

            ChangeMode(vehicle,"RTL")

            mode = "BACK"
        
    elif mode == "BACK":
        #--고도가 1 이하이면 착륙
        if vehicle.location.global_relative_frame.alt < 1.0:
            print("Vehicle landed, back to GROUND")
            mode = "GROUND"
    
    time.sleep(0.5)
