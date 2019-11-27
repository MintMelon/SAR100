import RPi.GPIO as GPIO
from time import sleep
import numpy as np

import math
# robot geometry in mm
e = 60.0    # end effector radius
f = 240.0   # base radius (2x dynamixel to dynamixel distance)
re = 200.0   # end to elbow dist
rf = 80.0   # base to elbow dist
 
# trigonometric constants
sqrt3 = math.sqrt(3.0)
pi = 3.141592653
sin120 = sqrt3/2.0
cos120 = -0.5    
tan60 = sqrt3
sin30 = 0.5
tan30 = 1/sqrt3

# inverse kinematics
 # helper functions, calculates angle theta1 (for YZ-pane) in degrees
def delta_calcAngleYZ(x0, y0, z0):
    y1 = -0.5 * 0.57735 * f # f/2 * tg 30
   # print("y1",y1)
    y0 -= 0.5 * 0.57735 * e # shift center to edge
    #print("y0",y0)
    # z = a + b*y
    a = (x0*x0 + y0*y0 + z0*z0 +rf*rf - re*re - y1*y1)/(2*z0)
   # print("a",a)
    b = (y1-y0)/z0
    #print("b",b)
    # discriminant
    d = -(a+b*y1)*(a+b*y1)+rf*(b*b*rf+rf)
   # print("d",d)
    if d < 0:
        return (-1, 0) # non-existing point
    yj = (y1 - a*b - (d**.5))/(b*b + 1) # choosing outer point
   # print("yj",yj)
    zj = a + b*yj
    #print("zj",zj)
    #theta = 180.0*atan(-zj/(y1 - yj))/pi + ((yj>y1)?180.0:0.0)
    if (yj>y1):
        theta = 180.0*math.atan(-zj/(y1 - yj))/pi + 180.0
    else:
        theta = 180.0*math.atan(-zj/(y1 - yj))/pi + 0.0
    return (theta)
def IK(X0,Y0,Z0):
    theta1_global = delta_calcAngleYZ(X0,Y0,Z0)
    theta2_global = delta_calcAngleYZ(X0*np.cos(np.deg2rad(120)) + Y0*np.sin(np.deg2rad(120)), Y0*np.cos(np.deg2rad(120))-X0*np.sin(np.deg2rad(120)), Z0)
    theta3_global = delta_calcAngleYZ(X0*np.cos(np.deg2rad(120)) - Y0*np.sin(np.deg2rad(120)), Y0*np.cos(np.deg2rad(120))+X0*np.sin(np.deg2rad(120)), Z0)
    
    return theta1_global , theta2_global , theta3_global





GPIO.setmode(GPIO.BOARD)

GPIO.setup(11,GPIO.OUT)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)


pwm1=GPIO.PWM(11, 50)
pwm2=GPIO.PWM(3, 50)
pwm3=GPIO.PWM(5, 50)
pwm1.start(0)
pwm2.start(0)
pwm3.start(0)

def setangle(angle1, angle2, angle3):
    if angle1<0:
        angle1 = angle1 *(-1)
    if angle2<0:
        angle2= angle2 *(-1)
    if angle3<0:
        angle3 = angle3 *(-1)
    duty1 = (angle1/18) + 2.5
    duty2 = (angle2/18) + 2.5
    duty3 = (angle3/18) + 2.5


# left -90 deg position

    pwm1.ChangeDutyCycle(duty1)# left -90 deg position
    pwm2.ChangeDutyCycle(duty2)
    pwm3.ChangeDutyCycle(duty3)
    sleep(1)
    pwm1.ChangeDutyCycle(12.5)# left -90 deg position
    pwm2.ChangeDutyCycle(12.5)
    pwm3.ChangeDutyCycle(12.5)
    sleep(1)
angles = [[40,50,175],[39,45,160],[23,46,200],[40,50,175],[50,30,180],[20,50,200],[35,10,230],[10,20,160],[16,55,200],[49,23,190],[5,45,175],[19,40,183],[50,5,205],[43,49,145],[40,50,175],[44,9,155],[39,30,195],[27,30,250],[50,10,165],[36,20,260],[24,10,145],[11,12,175],[34,29,146],[32,43,211],[4,50,260],[34,34,134],[4,7,175]]
for x in angles:
        angle1,angle2,angle3 = IK(x[0], x[1],x[2])
        setangle(angle1,angle2,angle3)
pwm1.stop()
pwm2.stop()
pwm3.stop()

GPIO.cleanup()

    