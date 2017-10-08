# Import opencv and pin_output_library
import os
import cv2
import math
from grip import VisionPipeline

import Adafruit_PCA9685

fovx = 40
fovy = 30


#ticks 0 to 180
xtickMin = 150
xtickMax = 575
xservorange = 180

# Convert angle to servos values
xtickrange = xtickMax - xtickMin
xMiddle = xtickrange / 2
xoffset = xMiddle + xtickMin
xfovtickRange = xtickrange * fovx / xservorange  ##180 is total range of servo in x
xticktoFov = xfovtickRange  / fovx

#ticks 0 to  90
ytickMin = 285
ytickMax = 510
yservorange = 90

ytickrange = ytickMax - ytickMin
yMiddle = ytickrange / 2
yoffset = yMiddle + ytickMin
yfovtickRange = ytickrange * ( float(fovy) / yservorange ) ##90 is total range of servo in y
yticktoFov = yfovtickRange  / fovy

print(yservorange, fovy)
#angletotick(angle, tickoffset, tick Mulitipiler, direction of motor)
def angletotick(xangle, offset, ticktoFov, direction):
    xo = (ticktoFov * (xangle * direction) + offset) 
    #print(ticktoFov)
    return int(xo)



angley = 0 ##set minimum value for y because it cannot travel passed 0
#Function to get the angle

#find_angle(pixel of target, resolution on camera, fov of camera)
def find_angle(pixel, resolution, fov):
    center = pixel - (resolution / 2)
    fovtoradains = (math.pi/180) * fov
    ratio = center * (math.sin(.5 * fovtoradains) / (.5 * resolution))
    radians = math.asin(ratio)
    out = (180 / math.pi) * radians
   # print("Angle: ", int(out), "Pixel :" , pixel) ## Debug print
    return out

pwm = Adafruit_PCA9685.PCA9685()

pwm.set_pwm_freq(60)

# Initialize servos
# Initialize opcv
# Initialize image pipline
pipeline = VisionPipeline()
WINDOW_NAME = "Vision Targeting"
# Initialize window
#cv2.namedWindow(WINDOW_NAME)
# Initialize camera
cap = cv2.VideoCapture(0)
while not cap.isOpened():
    # If the capture is not open
    cap.open(0)
read, image = cap.read()
print ("Capture opened")
os.system("sh /home/pi/Desktop/VisionTargetingSystem/test.sh")
os.system("sh /home/pi/Desktop/VisionTargetingSystem/test.sh")





while True: # cv2.getWindowProperty(WINDOW_NAME, 1) != -1: #True:
    # While the window has not been closed
    
    # Push image to window
   # cv2.imshow(WINDOW_NAME, image)
    cv2.waitKey(10)
    # Read image from the camera
    read, image = cap.read()
    if not read:
        # If image isn't reading
        print ("Image not read. Program no worky")
    # Image pipline goes here
    
    pipeline.process(image)
    
    if len(pipeline.convex_hulls_output) == 0:
        # If no convex hulls detected then restart while loop
        continue
    # After this for loop largest_hull is the target
    largest_hull = pipeline.convex_hulls_output[0]
    for hull in pipeline.convex_hulls_output:
        if cv2.contourArea(hull) > cv2.contourArea(largest_hull):
            largest_hull = hull
        
   
    # Find center points
    hull_moment = cv2.moments(largest_hull)
    center_x = int(hull_moment['m10']/hull_moment['m00'])
    center_y = int(hull_moment['m01']/hull_moment['m00'])
    cv2.circle(image,(center_x, center_y), 20, (0,0,0))
    
    #Init for vision angles to pwm

    resolutiony , resolutionx = image.shape[:2]
    
    #Cut off for y axis


    cameraAngley = find_angle(center_y, resolutiony, fovy)
    cameraAnlgex = find_angle(center_x, resolutionx, fovx)


    if cameraAngley > 0:
        angley =  0
    else:
        angley = cameraAngley
    
    servoY = angletotick(angley, yoffset, yticktoFov, 1)
    servoX = angletotick(cameraAnlgex, xoffset, xticktoFov, -1)

    #print(angley)
    # Set servos to values
    pwm.set_pwm(1,0,servoX) #angletotick(find_angle(center_x, resolutionx, fovx), xoffset, xticktoFov, -1))
    pwm.set_pwm(2,0, servoY) #angletotick(angley, yoffset, yticktoFov, 1))
    #print(angletotick(angley, yoffset, yticktoFov, 1))
   # print(fovy)
    #print(find_angle(center_y, resolutiony, fovy))
   # print(find_angle(center_x, resolutionx, fovx))
   # print(angletotick(find_angle(center_x, resolutionx, fovx), xoffset, xticktoFov, -1))
# Loop over
print ('Pre-camera release')
cap.release()
# Reset camera
cv2.destroyAllWindows()
#close window

print ('Program has ended')

