from twilio import TwilioRestException
from twilio.rest import TwilioRestClient

def run():
    # SID and Auth Token removed.
    account_sid = "{Twilio Account SID}"
    auth_token  = "{Twilio Account Auth Token}"

    client = TwilioRestClient(account_sid, auth_token)

    print("Sending message...")

    try:
        message = client.messages.create(body="Uh oh! Looks like someone is trying to get into your locked door.", from_="+14069480046", to="+14245422875")
    except TwilioRestException as e:
        print(e)

    print("Done!")