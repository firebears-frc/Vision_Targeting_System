# Import opencv and pin_output_library
import os
import cv2
import math
from grip import VisionPipeline

import Adafruit_PCA9685

xtickMin = 175 #0 to 180
xtickMax = 615


ytickMin = 217#0 to 90
ytickMax = 430

xtickrange = xtickMax - xtickMin
#range of xservo in ticks 0 to 180

xtick = ( 60/180 ) * xtickrange
#xtick should be 1/3 of the range

xangletotick = xtick / 60 #Need to change the 60 value to fov


v1 = xtick + xtickMin
v2 = ( xtick * 2 ) + xtickMin

##print(v1, v2)


def angletotick(xangle):
    xo = 2.44 * -xangle + 385 ##xangletotick 
##    print("Tick: ",int(xo))
    return int(xo)

##print(angletotick(30))


##degreetotickx =  (xMax -xMin)
##op = (degreetotickx / (xMax - xMin))
##print(op)
##degreetoticky =  90/(yMax - yMin)

pwmM = .75
xshift = 400
yshift = 217

fovx = 60
fovy = 50
angley = 0

def find_angle(pixel, resolution, fov):
    center = pixel - (resolution / 2)
    fovtoradains = (math.pi/180) * fov
    ratio = center * (math.sin(.5 * fovtoradains) / (.5 * resolution))
    radians = math.asin(ratio)
    out = (180 / math.pi) * radians
    print("Angle: ", int(out), "Pixel :" , pixel)
    return out

def fa(pixel, resolution, fov):
    center = pixel - (resolution / 2)
    angle = center * (fov/resolution)
    return angle

pwm = Adafruit_PCA9685.PCA9685()

pwm.set_pwm_freq(60)

# Initialize servos
# Initialize opcv
# Initialize image pipline
pipeline = VisionPipeline()
WINDOW_NAME = "Vision Targeting"
# Initialize window
cv2.namedWindow(WINDOW_NAME)
# Initialize camera
cap = cv2.VideoCapture(0)
while not cap.isOpened():
    # If the capture is not open
    cap.open(0)
read, image = cap.read()
print ("Capture opened")

os.system("v4l2-ctl --set-ctrl=exposure_auto=1")
os.system("v4l2-ctl --set-ctrl=exposure_absolute=60")
while cv2.getWindowProperty(WINDOW_NAME, 1) != -1:
    # While the window has not been closed
    
    # Push image to window
    cv2.imshow(WINDOW_NAME, image)
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
    if find_angle(center_y, resolutiony, fovy) < 0:
        angley = angley * 0
    else:
        angley = find_angle(center_y, resolutiony, fovy)
    
    # Convert angle to servos values
    pwmy = (angley * pwmM) + yshift
##    pwmx = (find_angle(center_x, resolutionx, fovx) * pwmM) + xshift
    
    # Set servos to values
    pwm.set_pwm(1,0,angletotick(find_angle(center_x, resolutionx, fovx)))
    ##pwm.set_pwm(2,0,int(pwmy))
##    print(angletotick(find_angle(center_x, resolutionx, fovx)))
# Loop over
print ('Pre-camera release')
cap.release()
# Reset camera
cv2.destroyAllWindows()
#close window

print ('Program has ended')