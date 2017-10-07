import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()

pwm.set_pwm_freq(60)

while True:
    x = int(input('Number: '))
##    y = int(input('Number2: '))
##    pwm.set_pwm(2,0,x)
    pwm.set_pwm(2,0,x)