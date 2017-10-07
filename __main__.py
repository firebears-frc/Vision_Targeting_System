# Import opencv and pin_output_library
import cv2
import math
from grip import VisionPipeline

import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()

pwm.set_pwm_freq(60)

#import Adafruit_PCA9685
#import pin_output_library

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
    
    fovx = 60
    fovy = 45
    y4 = 0
    resolutiony , resolutionx = image.shape[:2]
    
    fovRx = (math.pi/180) * fovx
    x2 = center_x - (resolutionx / 2)
    x3 = x2 * ((-1*math.sin(.5 * fovRx))/( .5 * resolutionx))
    radains = math.asin(x3)
    anglex = (180/math.pi) * radains

##    print(anglex)
    x4 = anglex +(0.5*fovx)
##    print(int(x4))
    pwmx = (x4 * 2.7) + 350
    
    pwm.set_pwm(1,0,int(pwmx))
    
    
    fovRy = (math.pi/180) * fovy
    y2 = center_y - (resolutiony / 2)
    y3 = y2 * ((1*math.sin(.5 * fovRy))/( .5 * resolutiony))
    radains = math.asin(y3)
    angley = (180/math.pi) * radains

##    print(anglex)
    if y4 < 0:
        y4 = angley * 0
    else:
        y4 = angley +(0.5*fovy)
##    print(int(y4))
    pwmy = (y4 * 2.7) + 200
    print(pwmy)
    pwm.set_pwm(2,0,int(pwmy))

    
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