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
    
    # Mode Basic, Advanced, Joystick:
    # Pour le moment, ne change que la force de chute quand aucune touche n'est appuyee
    MODE = "Joystick"
    
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
    
    Joystick = cont.sensors['Joystick']
    
    MotFrontRight = cont.actuators['MotFrontRight']
    MotFrontLeft = cont.actuators['MotFrontLeft']
    MotRearRight = cont.actuators['MotRearRight']
    MotRearLeft = cont.actuators['MotRearLeft']
    
    # BEHAVIOR MODEL
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
        
   
    # JOYSTICK
    if MODE == "Joystick":
        # FRONT/BACK
        front = Joystick.axisValues[1]/65534
        ForceRearRight -= front * FORCE_TANGAGE
        ForceRearLeft -= front * FORCE_TANGAGE
        ForceFrontRight += front * FORCE_TANGAGE
        ForceFrontLeft += front * FORCE_TANGAGE
        key_pressed = True
        
        # LEFT/RIGHT
        left = Joystick.axisValues[0]/65534
        ForceRearRight -= left * FORCE_TANGAGE
        ForceRearLeft += left * FORCE_TANGAGE
        ForceFrontRight -= left * FORCE_TANGAGE
        ForceFrontLeft += left * FORCE_TANGAGE
        key_pressed = True
        
        # LACET
        lacet = Joystick.axisValues[2]/65534
        ForceRearRight += lacet * FORCE_TANGAGE
        ForceRearLeft -= lacet * FORCE_TANGAGE
        ForceFrontRight -= lacet * FORCE_TANGAGE
        ForceFrontLeft += lacet * FORCE_TANGAGE
        key_pressed = True
            
        # DOWN (with the gaz knob)
        up = Joystick.axisValues[3]/65534
        uppos = -up + 0.5
        ForceFrontRight += uppos * FORCE_UP_JOYSTICK
        ForceFrontLeft += uppos * FORCE_UP_JOYSTICK
        ForceRearRight += uppos * FORCE_UP_JOYSTICK
        ForceRearLeft += uppos * FORCE_UP_JOYSTICK
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
            ForceFrontLeft = 0.5 * GRAVITY/4
            ForceFrontRight = 0.5 * GRAVITY/4
            ForceRearLeft = 0.5 * GRAVITY/4
            ForceRearRight = 0.5 * GRAVITY/4
    
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