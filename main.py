#################################### 
# IoT 2-Factor-Auth Door Lock (Facial + Voice Recognition)
# Kevin Leung @KSLHacks (Git: KSLHacks)
# James Earle @ItsJamesIRL (Git: JamesEarle)
# 9/12/2016

########### Python 2.7 #############
#!/usr/bin/python
# send_text option feature.. already implemented
# import send_text as st
import audio as a
import faceRecognition as f
import RPi.GPIO as GPIO
import os
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.OUT) # face green
GPIO.setup(22, GPIO.OUT) # face red
GPIO.setup(17, GPIO.OUT) # voice green
GPIO.setup(27, GPIO.OUT) # voice red

# Flash all LEDs - Testing purposes + Signal Hardware/Script is running
GPIO.output(18, GPIO.LOW)
GPIO.output(22, GPIO.LOW)
GPIO.output(17, GPIO.LOW)
GPIO.output(27, GPIO.LOW)
time.sleep(0.5)
GPIO.output(18, GPIO.HIGH)
GPIO.output(22, GPIO.HIGH)
GPIO.output(17, GPIO.HIGH)
GPIO.output(27, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(18, GPIO.LOW)
GPIO.output(22, GPIO.LOW)
GPIO.output(17, GPIO.LOW)
GPIO.output(27, GPIO.LOW)
time.sleep(0.5)
GPIO.output(18, GPIO.HIGH)
GPIO.output(22, GPIO.HIGH)
GPIO.output(17, GPIO.HIGH)
GPIO.output(27, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(18, GPIO.LOW)
GPIO.output(22, GPIO.LOW)
GPIO.output(17, GPIO.LOW)
GPIO.output(27, GPIO.LOW)

# Face green
GPIO.output(18, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(18, GPIO.LOW)

# Face red
GPIO.output(22, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(22, GPIO.LOW)

# Voice green
GPIO.output(17, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(17, GPIO.LOW)

# Voice red
GPIO.output(27, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(27, GPIO.LOW)

old_input = GPIO.input(23)

try:
    while True:
        new_input = GPIO.input(23)

        # Check for state change (button press)
        if(new_input != old_input):
            print("BUTTON PRESS")
            # flash both face green and red to signify picture in progress
	        GPIO.output(18, GPIO.HIGH)
            GPIO.output(22, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(18, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)

            # Take a photo using the Raspberry Pi camera
            os.system("raspistill -o output.jpg -q 40")
            
            # Use the photo we just took and verify with API
            print("Verifying face...")
            if(f.faceVerify()):
                print("Success - Face!")
                # Face is a success - signify by lighting green face
                GPIO.output(18, GPIO.HIGH)
                time.sleep(1)

                # Now test voice
                # flash both voice green and red to signify voice in progress
                GPIO.output(17, GPIO.HIGH)
                GPIO.output(27, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(17, GPIO.LOW)
                GPIO.output(27, GPIO.LOW)

                if(a.voiceVerify()):
                    print("Success - Voice!")
                    GPIO.output(17, GPIO.HIGH)
                    break
                else:
                    print("Failure - Voice!")
                    GPIO.output(27, GPIO.HIGH)
                    break
            else:
                # Failed to verify, send text and return
                print("Failure - Face!")
                GPIO.output(22, GPIO.HIGH)
                time.sleep(3)
                # texting functionality commented out for this demo - refer to implementation for details
                #st.run()
                break
            time.sleep(0.2)
finally:

    # hold this finished position until button is pressed again to end the program
    old_input = GPIO.input(23)
    while True:
        new_input = GPIO.input(23)

        # Check for state change (button press)
        if(new_input != old_input):
            break
        else:

    # Turn of LEDs
    GPIO.output(18, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(18, GPIO.HIGH)
    GPIO.output(22, GPIO.HIGH)
    GPIO.output(17, GPIO.HIGH)
    GPIO.output(27, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(18, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(18, GPIO.HIGH)
    GPIO.output(22, GPIO.HIGH)
    GPIO.output(17, GPIO.HIGH)
    GPIO.output(27, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(18, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)

    print("Finished")