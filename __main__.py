# Import opencv and pin_output_library
import cv2
import math
from grip import VisionPipeline

import Adafruit_PCA9685


fovx = 60
fovy = 45
angley = 0

def find_angle(pixel, resolution, fov):
##    print(pixel, resolution, fov)
    center = pixel - (resolution / 2)
    ratio = center * (math.sin(.5 * fov) / (.5 * resolution))
    radians = math.asin(ratio)
    angle = (180 / math.pi) * radians
    print(angle)
    
##    angle = (180 / math.pi) * (math.asin(pixel - (resolution / 2)) * ((math.sin(.5 * fov))/(.5 * resolution))) + (0.5*fovx)
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
   
    
    
##    #Convert the field of view from anlges to radains
##    fovRx = (math.pi/180) * fovx
##    fovRy = (math.pi/180) * fovy
##    
##    #Get values from the camera and convert them into negative and positve
##    x2 = center_x - (resolutionx / 2)
##    #Input the values above and finds the side of one triangle(sohcahtoa)
##    x3 = x2 * ((-1*math.sin(.5 * fovRx))/( .5 * resolutionx))
##    #Finds the angle with the side ratio
##    radains = math.asin(x3)
##    #Convert to degrees
##    anglex = (180/math.pi) * radains
##    #Convert to negative positve range fov where zero is middle 
##    x4 = anglex +(0.5*fovx)
##    
##    pwmx = (x4 * 2.7) + 350
##    pwm.set_pwm(1,0,int(pwmx))
##    
##    
##    
##    y2 = center_y - (resolutiony / 2)
##    y3 = y2 * ((1*math.sin(.5 * fovRy))/( .5 * resolutiony))
##    radains = math.asin(y3)
##    angley = (180/math.pi) * radains
##    resolutiony , resolutionx = image.shape[:2]
    resolutiony , resolutionx = image.shape[:2]

    if find_angle(center_y, resolutiony, fovy) < 0:
        angley = angley * 0
    else:
        angley = find_angle(center_y, resolutiony, fovy)
        
    pwmy = (-angley * 2.7) + 200
    pwm.set_pwm(2,0,int(pwmy))
    
    
##    print(find_angle(center_y, resolutiony, fovy))

    pwmx = (find_angle(center_x, resolutionx, fovx) * 2.7) + 350
    pwm.set_pwm(1,0,int(pwmx))

    
     # Find angle
     # Find angle

        # Convert angle to servos values
    
        # Set servos to values

        # Loop again
   
# Loop over
print ('Pre-camera release')
cap.release()
# Reset camera
cv2.destroyAllWindows()
#close window

print ('Program has ended')