#!/usr/bin/python
import send_text as st
import faceRecognition as f
import RPi.GPIO as GPIO
import os
import time

# Can't use this import, not supported on the Raspberry Pi without certain hardware
# import audio as a

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) # button
GPIO.setup(18, GPIO.OUT) # face green
GPIO.setup(22, GPIO.OUT) # face red
GPIO.setup(17, GPIO.OUT) # voice green
GPIO.setup(27, GPIO.OUT) # voice red

# Flash all LEDs
def flashAll():
    GPIO.output(18, GPIO.HIGH)
    GPIO.output(22, GPIO.HIGH)
    GPIO.output(17, GPIO.HIGH)
    GPIO.output(27, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(18, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
    GPIO.output(17, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)

# Flash the given LED
def flashIndividual(pin):
    GPIO.output(pin GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(pin, GPIO.LOW)

# Face green
flashIndividual(18)

# Face red
flashIndividual(22)

# Voice green
flashIndividual(17)

# Voice red
flashIndividual(27)

flashAll()

# Listen for button press
old_input = GPIO.input(23)

try:
    while True:
        new_input = GPIO.input(23)

        # Check for state change (button press)
        if(new_input != old_input):
            print("BUTTON PRESS")
            flashIndividual(18)

            # Take a photo using the Raspberry Pi camera
            os.system("raspistill -o output.jpg -q 40")
            
            # Use the photo we just took and verify with API
            print("Verifying face...")
            if(f.faceVerify()):
                print("Success!")
                # Face is a success, now perform voice
                GPIO.output(18, GPIO.HIGH)
                time.sleep(1)
                break
                # We don't have necessary hardware to implement voice
                # but we did implement the logic in audio.py

                # if(a.voiceVerify()):
                #     GPIO.output(321, GPIO.HIGH)
                #     both successful, flash lights
                #     and turn a motor to unlock door
            else:
                # Failed to verify, send text and return
                print("Failure!")
                
                # Visual feedback on failure
                for i in range(0, 3):
                    flashIndividual(22)
                    time.sleep(0.5)

                time.sleep(3)
                st.run()
                break
            time.sleep(0.2)
finally:
    # Flash all LEDs to signal end of program
    for i in range(0, 3):
        flashAll()

    print("Finished")