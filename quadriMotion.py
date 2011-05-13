import bge
from math import sqrt

def main():
    
    # CONSTANTE
    GRAVITY = 9.800
    MOTOR_MAX = 5
    RAYON = 1
    RATIO = sqrt(2)/2
    LACET = 1
    F = (1.3 * GRAVITY)/4
    FDOWN = (0.2 * GRAVITY)/4
    
    MODE = "Basic"
    
    # INIT
    cont = bge.logic.getCurrentController()
    own = cont.owner
    
    ForceFrontRight = 0
    ForceFrontLeft = 0
    ForceRearRight = 0
    ForceRearLeft = 0
    

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
    if keyZ.positive:
        ForceFrontRight += F
        ForceFrontLeft += F
        ForceRearRight += F
        ForceRearLeft += F
        
    if keyS.positive:
        ForceFrontRight += -FDOWN
        ForceFrontLeft += -FDOWN
        ForceRearRight += -FDOWN
        ForceRearLeft += -FDOWN
        
    if keyQ.positive: 
        ForceFrontRight += 1
        ForceFrontLeft -= 1
        ForceRearRight -= 1
        ForceRearLeft += 1
        
    if keyD.positive:
        ForceFrontRight -= 1
        ForceFrontLeft += 1
        ForceRearRight += 1
        ForceRearLeft -= 1
        
    if keyUp.positive:
        ForceRearRight += F
        ForceRearLeft += F

    if keyDown.positive:
        ForceFrontRight += F 
        ForceFrontLeft += F

    if keyLeft.positive:
        ForceFrontRight += F 
        ForceRearRight += F

    if keyRight.positive:
        ForceFrontLeft += F
        ForceRearLeft += F
        
    # BASIC MODEL
    if key4.positive:
        ForceFrontLeft += F
    if key5.positive:
        ForceFrontRight += F
    if key1.positive:
        ForceRearLeft += F
    if key2.positive:
        ForceRearRight += F    
    
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
    
        MotFrontLeft.force = [0, 0, ForceFrontLeft] 
        MotFrontLeft.torque = [ForceFrontLeft * RATIO, ForceFrontLeft * RATIO, - ForceFrontLeft * LACET]
        
        MotFrontRight.force = [0, 0, ForceFrontRight]
        MotFrontRight.torque = [ForceFrontRight * RATIO, -1 * ForceFrontRight * RATIO, ForceFrontRight * LACET] 
        
        MotRearRight.force = [0, 0, ForceRearRight]
        MotRearRight.torque = [-1 * ForceRearRight * RATIO, -1 * ForceRearRight * RATIO, -ForceRearRight * LACET]
         
        MotRearLeft.force = [0, 0, ForceRearLeft]
        MotRearLeft.torque = [-1 * ForceRearLeft * RATIO, ForceRearLeft * RATIO, ForceRearLeft * LACET] 

main()