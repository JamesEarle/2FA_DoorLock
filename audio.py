# IoT 2-Factor-Auth Door Lock (Facial + Voice Recognition)
# Kevin Leung @KSLHacks (Git: KSLHacks)
# James Earle @ItsJamesIRL (Git: JamesEarle)
# 9/12/2016

import pyaudio
import wave
import sys
import httplib
import urllib
import base64

# James - Phrase "my name is unknown to you""
jamesVerificationId = "18000dcf-7dec-45cf-b600-9ebd50460be6"

# Kevin - Phrase "be yourself everyone else is already taken""
kevinVerificationId = "982c9ebe-1412-4f01-9428-f3eda464279a"

chunk = 1024
_format = pyaudio.paInt16
_channels = 1
_rate = 16000

samples = []

p = pyaudio.PyAudio()

# NOTE: API subscription key removed, to use this script you must 
# provide your own in the request headers below

# Request headers
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '{API-Key}'
}

# Request parameters
params = urllib.urlencode({
    'shortAudio': 'false'
})

# Record a specified length audio stream with PyAudio
def record(seconds):
    stream = p.open(format=_format, channels=_channels, rate=_rate, input=True, output=True, frames_per_buffer=chunk)

    print("Recording...")

    for i in range(0, _rate / chunk * seconds):
        data = stream.read(chunk)
        samples.append(data)

    print("Done!")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Return a binary string representation of the audio
    return b''.join(samples)

# Save the audio samples to a file 
def save(filename):
    wf = wave.open(filename, "wb")
    wf.setnchannels(_channels)
    wf.setsampwidth(p.get_sample_size(_format))
    wf.setframerate(_rate)
    wf.writeframes(b''.join(samples))
    wf.close()

# Call the cognitive services API to verify the voice recording
def voiceVerify():
    byte_data = record(5)
    save("verify.wav")

    f = open("verify.wav", "rb")

    body = []

    try:
        while True:
            line = f.readline()
            if not line: break
            body.append(line)
        body = b''.join(body)
    finally:
        f.close()
    
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        
        # By default using Kevin's ID. Can change to use either
        conn.request("POST", "/spid/v1.0/verify?verificationProfileId="+ kevinVerificationId +"&%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        print("***")    
        print(response.length)
        print(data)
        print("***")
        
        conn.close()

        if(response.length == 0): return False
        return True
    except Exception as e:
        print(e)
        return False
