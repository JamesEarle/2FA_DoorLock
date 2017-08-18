########### Python 2.7 #############
import httplib, urllib, base64
import os

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '<Cognitive Service Voice Subscription Key>,
}

params = urllib.urlencode({
})

print("****** RECORDING ********")

# Take a voice recording using the USB Device microphone for 10seconds
os.system("arecord -D plughw:1 -d 5 -f S16 -r 16000 voice_record.wav")

print("***** DONE RECORDING *******")

f = open("voice_record.wav", "rb")

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
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/spid/v1.0/verificationProfiles/<voice_id>/enroll?%s" % params, body,$
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
