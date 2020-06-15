from twilio.rest import Client

account_sid = '**************************'
auth_token = '***************************'

def sendmessage(url):
	client = Client(account_sid, auth_token)
	#message = client.messages \
	#    .create(
	#         body=url,
	#         from_='+13343445189',
	#         to='+919496685357'
	#     )
	print "notification sent"


'''
#the following code is for sending mms in twilio notifier
account_sid = '**********************'
auth_token = '*************************'
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body='This is the ship that made the Kessel Run in fourteen parsecs?',
         from_='+13343445189',
         media_url=['https://projectasiet.s3.ap-south-1.amazonaws.com/sreelakshmi2020-04-30+20%3A33%3A42.744272.jpeg'],
         to='+919496685357'
     )

print(message.sid)'''
