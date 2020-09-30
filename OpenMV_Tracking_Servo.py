# Face Detection Example
#
# This example shows off the built-in face detection feature of the OpenMV Cam.
#es pass. Additionally, your OpenMV Cam uses
# a data structure called the integra
# Face detection works by using themple area contrasts checks. For the built-in
# frontalface detector ce rar Cae Haar Cascade feature detector on an image. A
# Haar Cascade is a series of siimage to quickly execute each area
# contrast check in constant time (the reequirment for the integral image).
#there are 25 stages of checks with scades run fast because later stages are
# only evaluated if previous stagl ach stage having
# hundreds of checks a piece. Haason for feature detection being
# grayscale only is because of the spa
from pyb import Servo
import sensor, time, image,pyb
x_pos = 0 # default
y_pos =10 # default

x_min = -35
x_max = 35
y_max = 10
y_min = 90

x_gain = +1.00 # You have to tweak this value to stablize the control loop.
               # You also may need to invert the value if the system goes
               # in the wrong direction.
y_gain = +1.00 # You have to tweak this value to stablize the control loop.
               # You also may need to invert the value if the system goes
               # in the wrong direction.
xServo = Servo(1)
yServo = Servo(2)

# Reset sensor
sensor.reset()
x=0
y=0
z=0
a=0
i=303
j=303
# Sensor settings
sensor.set_contrast(3)
sensor.set_gainceiling(16)
# HQVGA and GRAYSCALE are the best for face tracking.
sensor.set_framesize(sensor.HQVGA)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.__write_reg(0x0C, sensor.__read_reg(0x0C) | (1 << 7))
# Load Haar Cascade
# By default this will use all stages, lower satges is faster but less accurate.
face_cascade = image.HaarCascade("frontalface", stages=25)
print(face_cascade)
led = pyb.LED(3)
# FPS clock
clock = time.clock()

while (True):
    clock.tick()
    led.on()
    # Capture snapshot
    img = sensor.snapshot()

    # Find objects.
    # Note: Lower scale factor scales-down the image more and detects smaller objects.
    # Higher threshold results in a higher detection rate, with more false positives.
    objects = img.find_features(face_cascade, threshold=0.75, scale_factor=1.25)


    x_error = int((x - (img.width()/2)+40)/2.3)
    y_error = int(y - (img.height()/2))
    #print(y_error)

    #print(int(x_error))
    # Draw objects
    for r in objects:
        #print(r)
        x=r[0]
        y=r[1]
        img.draw_rectangle(r)
    if x_error == -34:
        xServo.angle(0)
        #print(0)

    else:
        if x_error == z:
            i=i+1
            if i > 300:
                if x_error == z:
                    xServo.angle(0)
                    #print(0)
            else:
                if x_error > 30:
                    xServo.angle(int(30))
                elif x_error < -30:
                    xServo.angle(int(-30))
                #print(x_error)
        else:
            if x_error > 30:
                xServo.angle(int(-30))
            elif x_error < -30:
                xServo.angle(int(30))
            #print(x_error)
            print(-x_error)
            i=0

        z=x_error


    if y_error == a:
        j=j+1
        if j > 300:
            if y_error == a:
                yServo.angle(-80)
                #print(0)
        else:
            yServo.angle(int(y_error))
            #print(x_error)
    else:
        yServo.angle(int(y_error))
        #print(x_error)
        j=0

    a=y_error






    #xServo.angle(int(x_error))

    # Print FPS.
    # Note: Actual FPS is higher, streaming the FB makes it slower.
    #print(clock.fps())
