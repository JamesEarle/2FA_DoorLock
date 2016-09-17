#################################### 
# IoT 2-Factor-Auth Door Lock (Facial + Voice Recognition)
# Kevin Leung @KSLHacks (Git: KSLHacks)
# James Earle @ItsJamesIRL (Git: JamesEarle)
# 9/12/2016

########### Python 2.7 #############
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient

def run():
    account_sid = "{Twilio_sid}"
    auth_token  = "Twilio_token"

    client = TwilioRestClient(account_sid, auth_token)

    print("Sending message...")

    try:
        message = client.messages.create(body="Uh oh! Looks like someone is trying to get into your locked door.", from_="{phoneNumber}", to="{phoneNumber}")
        # message = client.messages.create(body="Uh oh! Looks like someone is trying to get into your locked door.", from_="{phoneNumber}", to="{phoneNumber}", media_url="https://c1.staticflickr.com/3/2899/14341091933_1e92e62d12_b.jpg")
    except TwilioRestException as e:
        print(e)

    print("Done!")