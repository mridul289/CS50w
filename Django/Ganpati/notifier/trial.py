from twilio.rest import Client

account_sid = 'AC59dfd75f7bd630a40391a2c1bac41b51'
auth_token = 'cdf48f538661e774061f70913a968a4e'
client = Client(account_sid, auth_token)

message = client.messages.create(
    to= 'whatsapp:+919301976777',
    from_= 'whatsapp:+14155238886',
    body= 'This is supposed to be an automated message'
)
