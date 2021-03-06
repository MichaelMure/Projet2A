import bge
from math import sqrt

def main():
    
    # CONSTANTE
    GRAVITY = 9.800
    RATIO = sqrt(2)/2
    
    FORCE_LACET = 1
    FORCE_UP = (1.3 * GRAVITY)/4
    FORCE_DOWN = (0.2 * GRAVITY)/4
    FORCE_TANGAGE = 5
    FORCE_MOTOR_MAX = 5
    FORCE_UP_JOYSTICK = 4
    
    # Mode Basic ou Advanced
    MODE = "Advanced"
    
    # INIT
    cont = bge.logic.getCurrentController()
    own = cont.owner
    
    ForceFrontRight = 0
    ForceFrontLeft = 0
    ForceRearRight = 0
    ForceRearLeft = 0
    key_pressed = False
    
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
    
    # ADVANCED MODEL
    if keyZ.positive:
        ForceFrontRight += FORCE_UP
        ForceFrontLeft += FORCE_UP
        ForceRearRight += FORCE_UP
        ForceRearLeft += FORCE_UP
        key_pressed = True
        
    if keyS.positive:
        ForceFrontRight -= FORCE_DOWN
        ForceFrontLeft -= FORCE_DOWN
        ForceRearRight -= FORCE_DOWN
        ForceRearLeft -= FORCE_DOWN
        key_pressed = True
        
    if keyQ.positive: 
        ForceFrontRight += 1
        ForceFrontLeft -= 1
        ForceRearRight -= 1
        ForceRearLeft += 1
        key_pressed = True
        
    if keyD.positive:
        ForceFrontRight -= 1
        ForceFrontLeft += 1
        ForceRearRight += 1
        ForceRearLeft -= 1
        key_pressed = True
        
    if keyUp.positive:
        ForceRearRight += FORCE_TANGAGE
        ForceRearLeft += FORCE_TANGAGE
        key_pressed = True

    if keyDown.positive:
        ForceFrontRight += FORCE_TANGAGE
        ForceFrontLeft += FORCE_TANGAGE
        key_pressed = True

    if keyLeft.positive:
        ForceFrontRight += FORCE_TANGAGE
        ForceRearRight += FORCE_TANGAGE
        key_pressed = True

    if keyRight.positive:
        ForceFrontLeft += FORCE_TANGAGE
        ForceRearLeft += FORCE_TANGAGE
        key_pressed = True
                
        
    # BASIC MODEL
    if key4.positive:
        ForceFrontLeft += FORCE_MOTOR_MAX
        key_pressed = True
    if key5.positive:
        ForceFrontRight += FORCE_MOTOR_MAX
        key_pressed = True
    if key1.positive:
        ForceRearLeft += FORCE_MOTOR_MAX
        key_pressed = True
    if key2.positive:
        ForceRearRight += FORCE_MOTOR_MAX
        key_pressed = True
    
    # NO KEY MOTION
    
    if not key_pressed:
        if MODE == "Basic":
            ForceFrontLeft = 0
            ForceFrontRight = 0
            ForceRearLeft = 0
            ForceRearRight = 0
        else:
            ForceFrontLeft = 0.8 * GRAVITY/4
            ForceFrontRight = 0.8 * GRAVITY/4
            ForceRearLeft = 0.8 * GRAVITY/4
            ForceRearRight = 0.8 * GRAVITY/4
            
            euler = own.localOrientation.to_euler()
            ForceFrontLeft -= euler.x * FORCE_TANGAGE
            ForceFrontRight -= euler.x * FORCE_TANGAGE
            ForceRearLeft +=  euler.x * FORCE_TANGAGE
            ForceRearRight += euler.x * FORCE_TANGAGE
            
            ForceFrontLeft -= euler.y * FORCE_TANGAGE
            ForceFrontRight += euler.y * FORCE_TANGAGE
            ForceRearLeft -=  euler.y * FORCE_TANGAGE
            ForceRearRight += euler.y * FORCE_TANGAGE 
    
    # FINAL MOTION
    MotFrontLeft.force = [0, 0, ForceFrontLeft]
    MotFrontLeft.torque = [ForceFrontLeft * RATIO, ForceFrontLeft * RATIO, - ForceFrontLeft * FORCE_LACET]
    
    MotFrontRight.force = [0, 0, ForceFrontRight]
    MotFrontRight.torque = [ForceFrontRight * RATIO, -1 * ForceFrontRight * RATIO, ForceFrontRight * FORCE_LACET]
    
    MotRearRight.force = [0, 0, ForceRearRight]
    MotRearRight.torque = [-1 * ForceRearRight * RATIO, -1 * ForceRearRight * RATIO, -ForceRearRight * FORCE_LACET]
     
    MotRearLeft.force = [0, 0, ForceRearLeft]
    MotRearLeft.torque = [-1 * ForceRearLeft * RATIO, ForceRearLeft * RATIO, ForceRearLeft * FORCE_LACET]

main()