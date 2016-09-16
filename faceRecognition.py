#################################### 
# IoT 2-Factor-Auth Door Lock (Facial + Voice Recognition)
# Kevin Leung @KSLHacks (Git: KSLHacks)
# James Earle @ItsJamesIRL (Git: JamesEarle)
# 9/12/2016

import httplib
import urllib
import base64
import json

# Here 2 requests are made, to detect a face in an image and then
# verify that face belongs to the given ID number. Both sets have
# their own headers and parameters
#
# NOTE: API subscription key removed, to use this script you must 
# provide your own in the request headers below

# Request headers
headersDetect = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '{API-Key}',
}

# Request parameters
paramsDetect = urllib.urlencode({
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
})

# Request headers
headersVerify = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '{API-Key}',
}

# Request parameters (empty for verification)
paramsVerify = urllib.urlencode({})

# Read the binary from the jpg file
def faceVerify():
    # Adjust this directory structure to suit your project.
    f = open("/home/pi/Documents/iotDoorLock/output.jpg", "rb")
    try: 
        bodyDetect = f.read()
    finally:
        f.close()

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/detect?%s" % paramsDetect, bodyDetect, headersDetect)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    faceDetectJson = json.loads(data)
    
    if(faceDetectJson == []): return False

    bodyVerify = "{\
    \"faceId1\":\"{control faceID}\",\
    \"faceId2\": \"" + faceDetectJson[0]["faceId"] + "\"}"

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/verify?%s" % paramsVerify, bodyVerify, headersVerify)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    faceVerifyJson = json.loads(data)
    return faceVerifyJson["isIdentical"]
