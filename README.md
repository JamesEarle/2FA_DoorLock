# IoT 2-Factor-Auth Door Lock (Facial + Voice Recognition)

2FA physical locking system using RaspberryPi2 with RP Camera V2 and microphone.

Photos and voice recordings are taken from the device, stored, and verified using the Microsoft Cognitive Services APIs to do identity detection.

There are two main parts to this project:

1. main.py
 1. Face Recognition
 2. Voice Recognition
2. Hardware Setup
 1. Resistors = 220(Ohm)
 2. Pushbutton
 3. RaspberryPi2 Camera V2
 4. Digital microphone (RP2 does not support analog)

![FritzingDiagram](Fritzing.png?raw=true "Fritzing Diagram")

![LogicFlow](logicFlow.PNG?raw=true "Logic Flow Diagram")