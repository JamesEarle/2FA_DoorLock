#################################### 
# IoT 2-Factor-Auth Door Lock (Facial + Voice Recognition)
# Kevin Leung @KSLHacks (Git: KSLHacks)
# James Earle @ItsJamesIRL (Git: JamesEarle)
# 9/12/2016

########### Python 2.7 #############
import json
import sys
import httplib
import urllib
import base64

# James - Phrase "my name is unknown to you""
identificationProfileId = ""
jamesVerificationId = ""

# Kevin - Phrase "be yourself everyone else is already taken""
kevinVerificationId = "<Create and enroll user. Id here>"

# Request headers
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '<Cognitive Service Voice Key Here>'
}

# Request parameters
params = urllib.urlencode({
})

# Call the cognitive services API to verify the voice recording
def voiceVerify():

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
        conn.request("POST", "/spid/v1.0/verify?verificationProfileId=" + kevinVerificationId + "&%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        print("***")    
        print(data)
        print("***")
        
        conn.close()
	
	#convert string to JSON
	d = json.loads(data)
        if(d['result'] == "Accept"): return True
        return False
    except Exception as e:
        print(e)
        return False
