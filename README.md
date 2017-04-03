# IoT 2-Factor-Auth Door Lock (Facial + Voice Recognition)

2FA physical locking system using RaspberryPi3 with RP Camera V2.1 and microphone.

Photos and voice recordings are taken from the device, stored, and verified using the Microsoft Cognitive Services APIs to do identity detection.

There are two main parts to this project:

1. main.py
    1. Face Recognition
    2. Voice Recognition
2. Hardware Setup
    1. RaspBerryPi 3 (RP2 will also work, keep in mind there is no built inwifi)
    2. Resistors = 220(Ohm)
    3. Pushbutton
    4. (2) Red LEDs, (2) Green LEDs
    5. RaspberryPi2 Camera V2.1
    6. Digital microphone (USB 7.1 channel audio + Microphone)

### Audio ###
- Great blog here: [Recording on Pi](http://www.g7smy.co.uk/2013/08/recording-sound-on-the-raspberry-pi/)
- Useful commands:
    - `alsamixer` - open up visual mixer
    - `sudo alsactl store 1` - store settings into a variable
    - `arecord -l` - view all available recording devices
    - `arecord` - for more help and options
    - `arecord –f S16 –r 16000 –D plughw:1 –d 5 ./voice_record.wav` - record with specific settings
    - `aplay ./voice_record.wav` - play back audio on pi

### Picture ###
- Enable the camera device
    1. sudo raspi-config
    2. Select ‘5 Enable Camera’
    3. Select ‘Yes’
    4. Select ‘Finish’ on main menu
- To take a picture.. (RaspberryPi Camera V2.1)
    - `raspistill –o output.jpg –q 40`

## Circuit Diagram ##

![FritzingDiagram](Fritzing.png?raw=true "Fritzing Diagram")

## Logic Flow Diagram ##

![LogicFlow](logicFlow.PNG?raw=true "Logic Flow Diagram")