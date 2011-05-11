import bge
from math import sqrt


def main():
    # CONSTANTE
    GRAVITY = 9.81
    MOTOR_MAX = 10
    RAYON = 1
    RATIO = sqrt(2)/2
    LACET = 0.5
    
    MODE = "Basic"
    
    # INIT
    cont = bge.logic.getCurrentController()
    own = cont.owner

    keyUp = cont.sensors['Up']
    keyDown = cont.sensors['Down']
    keyLeft = cont.sensors['Left']
    keyRight = cont.sensors['Right']
    keyZ = cont.sensors['Z']
    keyS = cont.sensors['S']
    keyQ = cont.sensors['Q']
    keyD = cont.sensors['D']
    
    key4 = cont.sensors['4']
    key5 = cont.sensors['5']
    key1 = cont.sensors['1']
    key2 = cont.sensors['2']
    
    MotFrontRight = cont.actuators['MotFrontRight']
    MotFrontLeft = cont.actuators['MotFrontLeft']
    MotRearRight = cont.actuators['MotRearRight']
    MotRearLeft = cont.actuators['MotRearLeft']
    
    # BEHAVIOR MODEL
    if keyUp.positive:
        MotFrontRight.force = [0, 0, 12]

    if keyDown.positive:
        MotFrontLeft.force = [0, 0, 12]

    if keyLeft.positive:
        MotRearRight.force = [0, 0, 12]

    if keyRight.positive:
        MotRearLeft.force = [0, 0, 12]
    
    
    # NO KEY MOTION
    MotFrontLeft.torque = [0, 0, 0]
    MotFrontRight.torque = [0, 0, 0]
    MotRearLeft.torque = [0, 0, 0]
    MotRearRight.torque = [0, 0, 0]
    
    if MODE == "Basic":
        MotFrontLeft.force = [0, 0, 0]
        MotFrontRight.force = [0, 0, 0]
        MotRearLeft.force = [0, 0, 0]
        MotRearRight.force = [0, 0, 0]
    else:
        MotFrontLeft.force = [0, 0, GRAVITY/4]
        MotFrontRight.force = [0, 0, GRAVITY/4]
        MotRearLeft.force = [0, 0, GRAVITY/4]
        MotRearRight.force = [0, 0, GRAVITY/4]
    
    # FINAL MOTION
    if MODE == "Basic":
        right = left = 0
        if key4.positive:
            MotFrontLeft.force = [0, 0, MOTOR_MAX]
            MotFrontLeft.torque = [MOTOR_MAX * RATIO, MOTOR_MAX * RATIO, -LACET]
        if key5.positive:
            MotFrontRight.force = [0, 0, MOTOR_MAX]
            MotFrontRight.torque = [MOTOR_MAX * RATIO, -1 * MOTOR_MAX * RATIO, LACET]
        if key1.positive:
            MotRearLeft.force = [0, 0, MOTOR_MAX]
            MotRearLeft.torque = [-1 * MOTOR_MAX * RATIO, MOTOR_MAX * RATIO, LACET]
        if key2.positive:
            MotRearRight.force = [0, 0, MOTOR_MAX]
            MotRearRight.torque = [-1 * MOTOR_MAX * RATIO, -1 * MOTOR_MAX * RATIO, -LACET]
        
        

main()