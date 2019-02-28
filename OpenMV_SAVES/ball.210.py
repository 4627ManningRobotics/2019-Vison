
import sensor, image, time, json,math
threshold_indexg =  0
threshold_indexr =  0
# 0 for red, 1 for green, 2 for blue
# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The below thresholds track in general red/green/blue things. You may wish to tune them...


thresholdsr = [(0, 99, -128, 68, 63, 100)]
thresholdsg = [(50, 100, -92, -35, -102, 74)]


from pyb import UART
from pyb import LED

red_led   = LED(1)
green_led = LED(2)
blue_led  = LED(3)

status = "running"
counter = 0
LED_ON = False

uart = UART(1, 115200, timeout_char=1000)                         # init with given baudrate
uart.init(115200, bits=8, parity=None, stop=1, timeout_char=1000)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 1000)
#gain = sensor.get_rgb_gain_db()  # Get current gain
#gain = (-6.02073, -3.555992, 3.246127)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False)# must be turned off for color tracking
sensor.set_auto_exposure(False)
sensor.set_brightness(-3)
sensor.set_saturation(3)
sensor.set_contrast(-3)

clock = time.clock()

def setStatus():
    global LED_ON
    if status == "running":
        if LED_ON:
            red_led.off()
            green_led.off()
            blue_led.off()
            LED_ON = False
        else:
            red_led.on()
            LED_ON = True
    elif status == "ball":
        if LED_ON:
            red_led.off()
            green_led.off()
            blue_led.off()
            LED_ON = False
        else:
            green_led.on()
            LED_ON = True
    elif status == "strips":
        if LED_ON:
            red_led.off()
            green_led.off()
            blue_led.off()
            LED_ON = False
        else:
            blue_led.on()
            LED_ON = True

def ball():
# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. "merge=True" merges all overlapping blobs in the image.

    global status
    img = sensor.snapshot()

    for blob in img.find_blobs([thresholdsr[threshold_indexr]], pixels_threshold= 20, area_threshold=20, merge=True):
             img.draw_rectangle(blob.rect())
             img.draw_cross(blob.cx(), blob.cy())
             angle=0
             status = "ball"
             setStatus()
             xpos=blob.cx()-44

        #
             if xpos<0: #gives me an angle based on a cartisian plane and the veiw of the camera
                angle = xpos*(49/80)*(0.0174533)
             else :
                angle = xpos* (49/80)*(0.0174533)

             y = (-0.0526042175*(blob.h())+2.8429260117)
             o = {
             'KEY' : 'BALL',
             'Y' : y,
             'Angle': angle}
             uart.write(json.dumps(o) + "\n")
             print ("ball" , angle)

def strips():


# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. "merge=True" merges all overlapping blobs in the image.
    global status
    img = sensor.snapshot()

    for blob in img.find_blobs([thresholdsg[threshold_indexg]], pixels_threshold=20, area_threshold=20, merge=True):
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        xpos=blob.cx()-160
        status = "strips"
        setStatus()

        if xpos<0 :
            angle = xpos*(49/80)*(0.0174533)
        else:
            angle = xpos* (49/80)*(0.0174533)
        y =  (-0.0379740879*(blob.h())+2.9046474843-0.3)
        o = {
        'KEY' : 'STRIP',
        'Y' : y,
        'Angle' : angle
        }

        uart.write(json.dumps(o) + "\n")


while (True):

    strips()
    ball()
    status = "running"
    counter = counter + 1
    if counter == 100:
        setStatus()
        counter = 0







