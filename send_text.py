from twilio import TwilioRestException
from twilio.rest import TwilioRestClient

def run():
    account_sid = "ACcb92d2f1964f41bf5e02791cfc580897"
    auth_token  = "9ae1564c746a9798044e43b467e3ac0b"

    client = TwilioRestClient(account_sid, auth_token)

    print("Sending message...")

    try:
        message = client.messages.create(body="Uh oh! Looks like someone is trying to get into your locked door.", from_="+14069480046", to="+14245422875")
        # message = client.messages.create(body="Uh oh! Looks like someone is trying to get into your locked door.", from_="+14069480046", to="+14245422875", media_url="https://c1.staticflickr.com/3/2899/14341091933_1e92e62d12_b.jpg")
    except TwilioRestException as e:
        print(e)

    print("Done!")